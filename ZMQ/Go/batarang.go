//Go implementation of batarang


package ARCAM

import (
    "net"
    "os"
    "os/signal"
    "io"
    "sync"
    "time"
    "fmt"
    "flag"
)


func check(e error) {
	if e != nil {
		fmt.Printf("ERROR: ", e.Error())
		panic(e)
	}
}

func pass(e error) {
	if e != nil {
		fmt.Printf("Passing error : ", e.Error())
	}
}


//Node structure for node data
type Node struct{
    IP   string
    ACK     bool
    Alive   bool
    hbTime  float32
}
//Message structure for message data
type Message struct{
    source  string
    msgType string
    msgDat  string
    time    string
}
//NodeTable structure
type NodeTable struct{
    startTime   float32
    header      string
    node_dict   map[string]Node
}

//Globals
var localNode Node

//Heart beats tell other nodes that current node is still alive
func beat(port int){
    
    BROADCAST_IPv4 := net.IPv4(192,168,200,255)
    socket, err := net.DialUDP("udp4", nil, &net.UDPAddr{
        IP:   BROADCAST_IPv4,
        Port: port,
    })
    check(err)
    defer socket.Close()
    
    for localNode.Alive {
        
        hb := Message(source = localNode.IP, msgType = "HB", msgDat = nil, time = (string) time.Now())
        _,err = socket.WritetoUDP(hb)
        pass(err)
        time.Sleep(1)
    }
}
//Stethescope listens on port for heartbeats and sends them through the channel
func stethescope(port int, hb_chan chan<- Message){
    
    socket, err := net.ListenUDP("udp4", &net.UDPAddr{
        IP:   net.IPv4(192,168,200, 0),
        Port: port,
    })
    check(err)
    defer socket.Close()
    var msg []byte
    for localNode,Alive {
        _,err := socket.ReadFromUDP(msg)
        pass (err)
        hb_chan <-(string) msg
    }
    
}

// Listen and pass messages on port to the msg channel
func listen(port int, msg_chan chan<- Message){
    
    socket, err := net.ListenUDP("udp4", &net.UDPAddr{
        IP:   net.IPv4(192,168,200, 0),
        Port: port,
    })
    check(err)
    defer socket.Close()
    var msg []byte
    for localNode,Alive {
        socket.ReadFromUDP(msg)
        msg_chan <-(string) msg
    }
    
}
//Our Loop waiting for input or a keyboard interrupt
func sendLoop(port int){   
    BROADCAST_IPv4 := net.IPv4(192,168,200,255)
    socket, err := net.DialUDP("udp4", nil, &net.UDPAddr{
        IP:   BROADCAST_IPv4,
        Port: port,
    })
    check(err)
    defer socket.Close()
    
    c:= make(chan os.Signal, 1)
    signal.Notify(c,os.Interrupt)
    defer close(c)
    
    in:= make(chan os.Signal, 1)
    signal.Notify(in,os.Stdin)
    defer close(in)
    
    for localNode.Alive {
        select{
            case <-in:
                msg := Message(localNode.name, "FC", "915000", (string) time.Now())
                _,err = socket.WritetoUDP(msg)
                pass(err)
            case <- c:
                localNode.Alive = false
                return
        }
    }
}
//Loop sorting chanels to specific processes
func handleMessages(hb_chan,msg_chan<-chan Message){
    for localNode.Alive{
        select{
            case hb <-hb_chan:
            //handle heartbeats
            case hb <-msg_chan:
            //handle other messages
        }
    }  
}


func main() {
    hb_port := 9001
    msg_port := 9000
    arg = flag.Arg(0)
    if arg == nil {
        arg = 'bat0'
    }
    
    
    iface, err := net.Interface()[arg]
    if err != nil {
        fmt.Printf("Available interfaces...", net.Interfaces())
    }
    check(err)
    
    IP, err := iface['addr']
    check(err)
    
    localNode = Node{IP,false,(float32)time.Now()}
    defer localNode.Alive = false
    
    msg_chan = make(chan Message)
    hb_chan = make(chan Message)
    
    go handleMessages(hb_chan, msg_chan)
    defer close(msg_chan)
    defer close(hb_chan)
    
    go heartbeats(hb_port)
    go stethescope(hb_port,hb_chan)
    
    
    go listen(msg_port, msg_chan) 
    //our sending loop
    sendLoop(msg_port)
}

