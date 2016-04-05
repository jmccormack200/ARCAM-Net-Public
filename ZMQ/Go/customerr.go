


package customerr


//error handling
func check(e error) {
	if e != nil {
		fmt.Println("ERROR: ", e.Error())
        localNode.Alive = false
		panic(e)
	}
}
func catchbyte(e error, dat []byte) {
	if e != nil {
		fmt.Println("ERROR: ", e.Error())
        fmt.Println("Periferal data: ", dat)
        localNode.Alive = false
		panic(e)
	}
}
func catchstring(e error, dat string) {
	if e != nil {
		fmt.Println("ERROR: ", e.Error())
        fmt.Println("Periferal data: ", dat)
        localNode.Alive = false
		panic(e)
	}
}
func pass(e error) {
	if e != nil {
		fmt.Println("Ignoring error: ", e.Error())
	}
}