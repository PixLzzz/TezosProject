# TezosProject

you will find : 

- A vote.ligo file in written with ligolang
- A vote_test.py file wich contains all the tests for each entry point
- a list of all the commands you need in order to compile/test/deploy the given contracts

---

## Compile contract

input : 
```shell
ligo compile-contract vote.ligo main > vote.tz
```

---

## Compile storage 

```shell
vote.ligo :

ligo compile-storage vote.ligo main 'record[status = True; yes = 0n; no = 0n; voters = (Set.empty : set(address))
```



---

## Dry-run examples  : 

### Vote function :



- Non-owner account : vote yes -> [ Success, +1 yes ]

```shell
ligo dry-run --sender="tz1gjaF81ZRRvdzjobyfVNsAeSC6PScjfQwN" vote.ligo main 'Vote(1n)' 'record[status = True; yes = 0n; no = 0n; voters = (Set.empty : set(address))]'
```



- Non-owner account : vote no -> [ Success, +1 no ]

```shell
ligo dry-run --sender="tz1gjaF81ZRRvdzjobyfVNsAeSC6PScjfQwN" vote.ligo main 'Vote(2n)' 'record[status = True; yes = 0n; no = 0n; voters = (Set.empty : set(address))]'
```


## Run tests with pytest & pyligo

You must install pytest and pytest-ligo first then you can run the command below 

```shell
make sure you're in you test file folder then  :

pytest vote_test.py
```

## Tezos-client 

### Originate your contract on chain

With the output of the command compile-storage you're able tooriginate your smart contract on chain

```shell
vote.tz :
tezos-client originate contract vote transferring 1 from account running ../path/vote.tz --init <insert result of ligo compile-storage> --burn-cap 0.667
```

### Get your contract storage 

You will need a tezos node, or a proxy to a tezos node.

```shell
tezos-client get contract storage for <mycontract>
```

### List all your contracts 

```shell
tezos-client list known contracts
```
