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
    In_channel.iter_lines stdin ~f:(fun line ->
        let words = String.split line ~on:' ' in
        let n_words = List.length words in
        total_words := !total_words + n_words;
        triloop h words;
    );
    T.filter_inplace h ~f:(fun ct -> ct > 4);
    let al = T.to_alist h 
        |> List.sort ~cmp
    in
    printf "%d\n" !total_words;
    List.iter al ~f:(fun (x, y) -> printf "%d %s\n" y x)

