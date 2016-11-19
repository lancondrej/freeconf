/**
 * Created by ondra on 19.11.16.
 */
namespace = '/freeconf';

// Connect to the Socket.IO server.
// The connection URL has the following format:
//     http[s]://<domain>:<port>[/<namespace>]
var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);