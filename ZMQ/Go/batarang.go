//Go implementation of batarang


package main

import (
    "net"
    "os"
    "os/signal"
    //"io"
    "bufio"
    "encoding/json"
    //"sync"
    "time"
    "fmt"
    "flag"
    "nodepkg"
    "customerr"
    
)

//Globals
var localNode Node
/*
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


//Node structure for node data
type Node struct{
    IP      net.IP
    ACK     bool
    Alive   bool
    hbTime  time.Time
}
//Message structure for message data
type Message struct{
    source  string
    msgType string
    msgDat  string
    time    string
}
func (msg Message) String() string{
    return (msg.source + " " + msg.msgType + " " + msg.msgDat + " " + msg.time)
}
//NodeTable structure
type NodeTable struct{
    startTime   time.Time
    header      string 
    nodeDict    map[string]*Node
    ready       bool
}
func (table NodeTable)handleMsg(msg Message){
    //case 1: Empty Table
    if table.header == ""{
        table.startTime = time.Now()
        table.header = msg.msgDat
        table.ready = false
        //go broadcast
    //case 2: Waiting Table with matching data
    }
    if msg.msgDat == table.header {
          //Case 2.1: node is in table
          if _,ok := table.nodeDict[msg.source]; ok{
              newtime,err := time.Parse(time.StampMilli,msg.time)
              catchstring(err, msg.String())
              table.nodeDict[msg.source].ACK = true
              table.nodeDict[msg.source].Alive = true
              table.nodeDict[msg.source].hbTime = newtime
          //Case 2.2: node is missing in table
          } else {
              newtime,err := time.Parse(time.StampMilli,msg.time)
              catchstring(err,msg.String())
              newNode := Node{
                  IP: net.ParseIP(msg.source),
                  ACK: true,
                  Alive: true,
                  hbTime: newtime,
               }
               table.nodeDict[msg.source] = &newNode
               fmt.Printf("Node %s added to table \n", msg.source)
          }
          fmt.Printf("ACK %v", msg.source)
          //Check Table
    }
}
func (table NodeTable)handleHB(msg Message){
    //Case 1: node is in table
    if _,ok := table.nodeDict[msg.source]; ok{
        newtime,err := time.Parse(time.StampMilli,msg.time)
        catchstring(err, msg.String())
        table.nodeDict[msg.source].Alive = true
        table.nodeDict[msg.source].hbTime = newtime
        
    //Case 2: node is missing in table
    } else {
        newtime,err := time.Parse(time.StampMilli,msg.time)
        catchstring(err,msg.String())
        newNode := Node{
            IP: net.ParseIP(msg.source),
            ACK: false,
            Alive: true,
            hbTime: newtime,
        }
        table.nodeDict[msg.source] = &newNode
        fmt.Printf("Node (%s) added to table\n", msg.source)
    }
}
*/
//Heart beats tell other nodes that current node is still alive
func heartbeats(port int) {
    
    BROADCASTIPv4 := net.IPv4(192,168,200,255)
    socket, err := net.DialUDP("udp4", nil, &net.UDPAddr{
        IP:   BROADCASTIPv4,
        Port: port,
    })
    check(err)
    defer socket.Close()
    
    var hb = Message{localNode.IP.String(), "HB", "none", time.StampMilli}
    
    for localNode.Alive{
        hb.time = time.Now().Format(time.StampMilli)
        
        data,err := json.Marshal(hb)
        catchbyte(err, data)
        
        _, err = socket.Write(data)
        pass(err)
        
        time.Sleep(1)
    }
}

//hbListen listens on port for heartbeats and sends them through the channel
func hbListen(port int, hbChan chan<- Message){
    
    socket, err := net.ListenUDP("udp4", &net.UDPAddr{
        IP:   net.IPv4(192,168,200, 0),
        Port: port,
    })
    check(err)
    defer socket.Close()

    
    for localNode.Alive {
        var data []byte
        _,err = socket.Read(data)
        catchbyte(err,data)
        
        msg := Message{}
        
        err = json.Unmarshal(data,msg)
        check (err)
        
        hbChan<- msg
    }
    
}

// Listen and pass messages on port to the msg channel
func listen(port int, msgChan chan<- Message){
    
    socket, err := net.ListenUDP("udp4", &net.UDPAddr{
        IP:   net.IPv4(192,168,200, 0),
        Port: port,
    })
    check(err)
    defer socket.Close()
    
   for localNode.Alive{
        var data []byte 
        
        _,err = socket.Read(data)
        catchbyte(err,data)
        
        msg := Message{}
        
        err = json.Unmarshal(data,msg)
        check (err)
        
        msgChan<- msg
    }
}

//Our Loop waiting for input or a keyboard interrupt
func sendLoop(port int, in <-chan Message, q <-chan os.Signal){   
    BROADCASTIPv4 := net.IPv4(192,168,200,255)
    socket, err := net.DialUDP("udp4", nil, &net.UDPAddr{
        IP:   BROADCASTIPv4,
        Port: port,
    })
    check(err)
    defer socket.Close()
    
    for localNode.Alive {
        select{
            case msg:= <-in:
                data,err := json.Marshal(msg)
                catchbyte(err, data)
                
                _, err = socket.Write(data)
                pass(err)
            case <-q:
                localNode.Alive = false
                return
        }
    }
}
//Loop sorting chanels to specific processes
func handleMessages(hbChan,msgChan<-chan Message){

    for localNode.Alive{
        select{
            case hb := <-hbChan:
                fmt.Println(hb)
                //handle heartbeats
            case msg := <-msgChan:
                fmt.Println(msg)
                //handle other messages
        }
    }  
}


func fakeMessage(input chan<- Message, q <-chan os.Signal){
    var msg = Message{localNode.IP.String(), "FC", "915000", time.Now().Format(time.StampMilli)}
    
    for{
        select{
            case <-q:
                localNode.Alive = false
                return 
            default:
                bufio.NewReader(os.Stdin).ReadBytes('\n')
                msg.time = time.Now().Format(time.StampMilli)
                input <- msg
        }
    }
}


func main() {
    hbPort := 9001
    msgPort := 9000
    arg := flag.Arg(0)
    if arg == ""{
        arg = "bat0"
    }
    
    //Parse Interface
    iface, err := net.InterfaceByName(arg)
    if err != nil{
        ifaces, err := net.Interfaces()
        fmt.Println("Available interfaces are...")  
        for _,i := range ifaces{
            fmt.Println(i.Name)
        }
        check(err)
    }
    
    var ip net.IP
    addrs, err := iface.Addrs()
    check(err)
    for _, addr:= range addrs{
        switch v := addr.(type){
            case *net.IPNet:
                ip = v.IP
            case *net.IPAddr:
                ip = v.IP
        }
    }
    


    //Local node initialization
    localNode = Node{ip,true,true,time.Now()}
    
    //Channels
    msgChan := make(chan Message)
    defer close(msgChan)
    
    hbChan := make(chan Message)
    defer close(hbChan)
    
    q:= make(chan os.Signal, 1)
    signal.Notify(q,os.Interrupt)
    defer close(q)
    
    in:= make(chan Message, 1)
    defer close(in)
    
    //Goroutines
    go handleMessages(hbChan, msgChan)
    //Heartbeats
    go heartbeats(hbPort)
    ///Listen for heartbeats
    go hbListen(hbPort,hbChan)
    //listen for messages
    go listen(msgPort, msgChan) 
    //Outgoing messages
    go sendLoop(msgPort,in,q)
    
    fakeMessage(in,q)
}

