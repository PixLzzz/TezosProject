const owner : address = ("tz1KqTpEZ7Yob7QbPE4Hy4Wo8fHG8LhKxZSx" : address);

//type voters is set(address)
type storage is record [
  status : bool;
  yes : nat;
  no : nat;
  voters : set(address);
]

type parameter is
| Vote of nat
| Reset of unit
| Stdby of string


type return is list (operation) * storage

// Function add_voters :
function add_voters (const store : storage) : storage is 
block { 
  store.voters := Set.add (sender, store.voters)
   } with store

// Function counter
function counter(const store : storage; const vote : nat) : storage is
block {
  if vote = 1n
    then store.yes := store.yes + 1n
  else if vote = 2n then
    store.no := store.no + 1n
  else skip;
} with store

function break (const stat : string; const store : storage) : storage is
 block { 
   if sender =/= owner
   then failwith("Access denied.")
   else if sender = owner and stat = "True"
      then 
        if stat = "True" then
          store.status := True
        else if stat = "False" then 
          store.status := False
        else skip;
    else skip;
    } with store

function vote (const vote : nat; const store : storage) : storage is
block {
    // check if the owner of the contract is trying to vote or
    // if someone who had already voted is trying to vote and
    // if the vote is open
    // if True -> failwith
  
    if sender = owner or store.voters contains sender or store.status = False
      then failwith ("Access denied.")
    else skip;
    
    // define a const who takes the numbers of input inside the set of voters then 
    // check if it's equal to 10
    const cardinal : nat = Set.size(store.voters);
    // if the set size of voter is >= to 10 we show the winner
    if cardinal >= 10n 
      then 
        if store.yes > store.no 
          then failwith("Yes won")
        else failwith("No won")
    else if cardinal = 9n 
      then {
        store := add_voters(store);
        if vote = 1n
          then store.yes := store.yes + 1n
        else if vote = 2n then
          store.no := store.no + 1n
        else skip;

        // after adding the 10th vote we get the result
        if store.yes > store.no 
          then failwith("Yes won")
        else failwith("No won");
        
        // we reach 10 vote we can now block the vote
        store.status := False;
      } 
    else {
      store := add_voters(store);
      if vote = 1n
        then store.yes := store.yes + 1n
      else if vote = 2n then
        store.no := store.no + 1n
      else skip;
    }
} with store
   

function reset (const store : storage) : storage is
block {
    const empty_set : set (address) = Set.empty;
    // check if the owner of the contract is trying to reset -> if True then reset the value
    if sender = owner and store.status = False then 
        store := store with record [
          status = True;
          yes = 0n;
          no = 0n;
          voters = empty_set;
        ]
    else failwith("Acces denied.")
  
} with store

function main (const action : parameter; const store : storage): return is
block {
  const new_storage : storage = case action of
    | Vote (n) -> vote (n, store)
    | Reset -> reset (store)
    | Stdby (n) -> break (n, store)
  end
} with ((nil : list (operation)), new_storage)
  