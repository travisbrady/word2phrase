open Core.Std
open Printf
module T=String.Table

let flip f x y = f y x
let cmp x y = (flip compare) (snd x) (snd y)

let rec triloop h lst =
    match lst with
    | a :: b :: c :: rest -> 
        T.incr h a;
        T.incr h (a ^ "_" ^ b);
        T.incr h (a ^ "_" ^ b ^ "_" ^ c);
        triloop h (b::c::rest)
    | a :: b :: rest -> 
        T.incr h a;
        T.incr h (a ^ "_" ^ b);
        triloop h (b::rest)
    | a :: rest ->
        T.incr h a;
        triloop h rest
    | [] -> ()

let () =
    let h = T.create () in
    let total_words = ref 0 in
    let line_no = ref 0 in
    eprintf "Start File Iter\n%!";
    In_channel.iter_lines stdin ~f:(fun line ->
        incr line_no;
        if !line_no mod 100_000 = 0 then eprintf "Line: %d\n%!" !line_no;
        let words = String.split line ~on:' '
            |> List.filter ~f:(fun x -> x <> "" && x <> " ")
        in
        let n_words = List.length words in
        total_words := !total_words + n_words;
        triloop h words;
    );
    eprintf "Done File Iter. Now Filter\n%!";
    T.filter_inplace h ~f:(fun ct -> ct > 4);
    eprintf "Done Filter. Now to_alist\n";
    let al = T.to_alist h 
        |> List.sort ~cmp
    in
    eprintf "Now Write file\n";
    printf "%d\n" !total_words;
    List.iter al ~f:(fun (x, y) -> printf "%s,%d\n" x y)


