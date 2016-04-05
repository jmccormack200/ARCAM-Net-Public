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
    "runtime"   
)

//Globals
var localNode Node
var nodeTable NodeTable
//Heart beats tell other nodes that current node is still alive
func heartbeats(port int) {
    BROADCASTIPv4 := net.IPv4(192,168,200,255)
    
    udpAddr:=&net.UDPAddr{
        IP:   BROADCASTIPv4,
        Port: port,
    }
    
    socket, err := net.DialUDP("udp4", nil, &net.UDPAddr{
        IP: net.IPv4zero,
        Port: 0,
    })
    check(err)
    defer socket.Close()
    
    var hb = Message{localNode.IP.String(), "HB", "none", time.StampMilli}
    
    for localNode.Alive{
        hb.time = time.Now().Format(time.StampMilli)
        
        data,err := json.Marshal(hb)
        catchstring(err, hb.String())
        
        n,oobn, err := socket.WriteMsgUDP(data,nil,udpAddr)
        fmt.Printf("%d::%d\n",n,oobn)
        pass(err)
        
        time.Sleep(time.Second * 1)
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
        data := make([]byte,1024)
        oob := make([]byte, 1024)
            
        n,oobn,flags,addr,err := socket.ReadMsgUDP(data, oob)
        fmt.Printf("%d::%d::%d::%v\n",n,oobn,flags,addr)
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
        data := make([]byte,1024)
            
        n,addr,err := socket.ReadFrom(data)
        fmt.Printf("%d::%v \n",n,addr)
        catchbyte(err,data)
        
        msg := Message{}
        
        err = json.Unmarshal(data,msg)
        catchbyte(err,data)
        
        msgChan<- msg
    }
}

// Broadcast messages
func broadcastMsg(msg Message, in chan<- Message){
    for nodeTable.ready == false{
        in <- msg
        time.Sleep(1)
    }
}

//Our loop waiting for input or a keyboard interrupt
func sendLoop(port int, in <-chan Message, q <-chan os.Signal){   
    BROADCASTIPv4 := net.IPv4(192,168,200,255)
    
    udpAddr:=&net.UDPAddr{
        IP:   BROADCASTIPv4,
        Port: port,
    }
    
    socket, err := net.DialUDP("udp4", nil, udpAddr)
    
    check(err)
    defer socket.Close()
    
    for localNode.Alive {
        select{
            case msg:= <-in:
                data := make([]byte,1024)
                
                data,err = json.Marshal(msg)
                catchstring(err, msg.String())
                
                n, err := socket.WriteTo(data, udpAddr)
                fmt.Printf("%d \n",n)
                pass(err)
                
            case <-q:
                localNode.Alive = false
                nodeTable.ready = false
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
                nodeTable.handleHB(hb)
                //handle heartbeats
            case msg := <-msgChan:
                fmt.Println(msg)
                //nodeTable.handleMsg(msg)
                //handle other messages
        }
    }  
}

func fakeMessage(input chan<- Message, q <-chan os.Signal){
    var msg = Message{localNode.IP.String(), "FC", "915000", ""}
    
    for localNode.Alive{
        select{
            case <-q:
                localNode.Alive = false
                nodeTable.ready = false
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
    
    //Global Initialization initialization
    localNode = Node{ip,true,true,time.Now()}
    nodeTable = NodeTable{time.Now(),"", make(map[string]*Node), false, 30}
    
    //Channels
    //msg in
    msgChan := make(chan Message)
    defer close(msgChan)
    
    //hb in
    hbChan := make(chan Message)
    defer close(hbChan)
    
    //quit channel
    q:= make(chan os.Signal, 1)
    signal.Notify(q,os.Interrupt)
    defer close(q)
    
    //msg out
    in:= make(chan Message, 1)
    defer close(in)
    
    //runtime
    runtime.GOMAXPROCS(runtime.NumCPU())
    
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
