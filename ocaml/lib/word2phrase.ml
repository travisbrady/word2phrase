open Core.Std
module T=String.Table

let foi = Float.of_int

let learn_vocab lst =
    let h = T.create () in
    let train_words = ref 0 in
    let rec aux _lst = 
        match _lst with
        | [] -> ()
        | [a] -> 
            incr train_words;
            T.incr h a
        | a :: b :: rest ->
            incr train_words;
            T.incr h a;
            T.incr h (a ^ "_" ^ b);
            aux (b::rest)
    in
    List.iter lst ~f:aux;
    h, foi(!train_words)

let filter_vocab vocab min_count =
    T.filter vocab ~f:(fun x -> x >= min_count)

let train_model lst min_count threshold =
    let vocab, train_words = learn_vocab lst in
    let vocab = filter_vocab vocab 5 in
    let rec aux _lst acc =
        match _lst with
        | [] -> List.rev acc
        | [a] -> List.rev (a::acc)
        | a :: b :: rest ->
            let pair = a ^ "_" ^ b in
            let score = 
                match (T.find vocab a, T.find vocab b, T.find vocab pair) with
                | (Some pa, Some pb, Some pab) ->
                    (foi (pab - min_count)) /. (foi pa) /. (foi pb) *. train_words
                | _ -> 0.0 
            in
            if score > threshold then
                aux rest (pair::acc)
            else
                aux (b::rest) (a::acc)
    in
    List.map lst ~f:(fun x -> aux x [])

