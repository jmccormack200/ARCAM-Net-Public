


package main

import(
    "fmt"
    "runtime"
)

//error handling
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
func catchbyte(e error, dat []byte) {
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
func catchstring(e error, dat string) {
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
func pass(e error) {
	if e != nil {
		fmt.Println("Ignoring error: ", e.Error())
	}
}