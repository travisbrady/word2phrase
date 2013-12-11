open Core.Std
open Printf
module T=String.Table
module M=String.Map

let flip f x y = f y x
let cmp x y= (flip compare) (snd x) (snd y)

let () =
    let h = T.create () in
    In_channel.iter_lines stdin ~f:(fun line ->
        let words = String.split line ~on:' ' in
        List.iter words ~f:(fun word -> T.incr h word)
    );
    let al = T.to_alist h 
        |> List.sort ~cmp
    in
    List.iter al ~f:(fun (x, y) -> printf "%d %s\n" y x)

