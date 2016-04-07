

//Custom error package
package main

import(
    "fmt"
    "runtime"
    "github.com/tendermint/go-p2p"
)

//error handling
//Throw error
func check(e error) {
	if e != nil {
		fmt.Println("ERROR: ", e.Error())
        _,file,line,_:= runtime.Caller(1)
        fmt.Printf("Location: File: %s Line: %d",file,line)
        localNode.Alive = false
        nodeTable.ready = false
        runtime.Goexit()
		panic(e)
	}
}
//Throw error and print input data that caused it
func catch(e error, dat interface{}) {
	if e != nil {
		fmt.Println("ERROR: ", e.Error())
        fmt.Println("Periferal data: ", dat)
        _,file,line,_:= runtime.Caller(1)
        fmt.Printf("Location: File: %s Line: %d",file,line)
        localNode.Alive = false
        nodeTable.ready = false
        runtime.Goexit()
		panic(e)
	}
}
//Ignore error but print warning
func pass(e error) {
	if e != nil {
		fmt.Println("Ignoring error: ", e.Error())
	}
}
