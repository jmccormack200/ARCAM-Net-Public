//Go implementation of batarang


package ARCAM

import (
    "net"
    "os"
    "os/signal"
    //"io"
    "bufio"
    "encoding/binary"
    "bytes"
    //"sync"
    "time"
    "fmt"
    "flag"
)


func check(e error) {
	if e != nil {
		fmt.Println("ERROR: ", e.Error())
		panic(e)
	}
}


func pass(e error) {
	if e != nil {
		fmt.Println("Passing error : ", e.Error())
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
    startTime   float32
    header      string
    nodeDict   map[string]Node
}

//Globals
var localNode Node

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
        
        buf := &bytes.Buffer{}
        err := binary.Write(buf, binary.BigEndian, hb)
        check(err)
        
        _, err = socket.Write(buf.Bytes())
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
        
        buf := &bytes.Buffer{}
        _,err := socket.Read(buf.Bytes())
        pass(err)
        
        msg := Message{}
        
        err = binary.Read(buf, binary.BigEndian, &msg)
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
        buf := &bytes.Buffer{}
        _,err := socket.Read(buf.Bytes())
        pass(err)
        
        msg := Message{}
        
        err = binary.Read(buf, binary.BigEndian, &msg)
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
                msg.time = time.Now().Format(time.StampMilli)
                
                buf := &bytes.Buffer{}
                err := binary.Write(buf, binary.BigEndian, msg)
                check(err)
                
                _, err = socket.Write(buf.Bytes())
                pass(err)
                
                time.Sleep(1)
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


func fakeMessage(input chan<- Message){
    var msg = Message{localNode.IP.String(), "FC", "915000", time.Now().Format(time.StampMilli)}
    
    for{
        bufio.NewReader(os.Stdin).ReadBytes('\n')
        msg.time = time.Now().Format(time.StampMilli)
        input <- msg
    }
}


func main() {
    hbPort := 9001
    msgPort := 9000
    arg := flag.Arg(0)
    if arg == " "{
        arg = "bat0"
    }
    
    //Parse Interface
    ifaces, err := net.Interfaces()
    check(err)
    var ip net.IP
    for _,i := range ifaces{
        if i.Name == arg {
            addrs, err := i.Addrs()
            check(err)
            for _, addr:= range addrs{
                switch v := addr.(type){
                    case *net.IPNet:
                        ip = v.IP
                    case *net.IPAddr:
                        ip = v.IP
                }
            }
        }
    }
    

    //Local node initialization
    var localNode = Node{ip,true,true,time.Now()}
    defer func(localNode Node){localNode.Alive = false}(localNode)
    
    
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
    
    fakeMessage(in)
}

