# batarang_go
--
#Go implementation of batarang


Custom error package

My Node struct package
// Emit the standard documentation (what godocdown would emit without a template)

# batarang_go
--
// Emit the package name and an import line (if one is present/needed)

#Go implementation of batarang


Custom error package

My Node struct package
// Emit the package declaration

## Usage

    const (
    	BROADCASTipv4 = "192.168.200.255"
    )

Constants

#### type Message

    type Message struct {
    }


Message structure for message data

#### func (Message) String

    func (msg Message) String() string

Convert message to String

#### type Node

    type Node struct {
    	IP    net.IP
    	ACK   bool
    	Alive bool
    }


Node structure for node data

#### type NodeTable

    type NodeTable struct {
    }


NodeTable structure
// Emit package usage, which includes a constants section, a variables section,
// a functions section, and a types section. In addition, each type may have its own constant,
// variable, and/or function/method listing.

 ... 
// A boolean indicating whether the given package is a command or a plain package

batarang_go
// The name of the package/command (string)

.
// The import path for the package (string)
// (This field will be the empty string if godocdown is unable to guess it)
