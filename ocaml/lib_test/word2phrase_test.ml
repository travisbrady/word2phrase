open Core.Std
module W=Word2phrase

let () =
    let lines = In_channel.read_lines (Sys.argv.(1)) in
    let tokenized = List.map lines ~f:(fun x -> String.split x ~on:' ') in
    let res1 = W.train_model tokenized 5 500.0 in
    let res2 = W.train_model res1 5 450.0 in
    let res3 = W.train_model res2 5 400.0 in
    let out_lines = List.map res3 ~f:(fun x -> String.concat ~sep:" " x) in
    Out_channel.write_lines "out" out_lines

