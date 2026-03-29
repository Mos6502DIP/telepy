import java.io.*;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.Objects;
import java.util.Scanner;

class TcpClient {

    private final String host;
    private final int port;

    private Socket socket;
    private InputStream in;
    private OutputStream out;

    public TcpClient(String host, int port) {
        this.host = host;
        this.port = port;
    }

    public void connect() throws IOException {
        socket = new Socket(host, port);
        socket.setTcpNoDelay(true);
        in = socket.getInputStream();
        out = socket.getOutputStream(); // Creates a socket connection and declares in and out data streams for messages

        System.out.println("Connected to " + host + ":" + port);
    }

    public void send(String message) throws IOException {
        byte[] data = message.getBytes(StandardCharsets.UTF_8);
        out.write(data);
        out.flush(); // Send as string to the server
    }

    public void ack() throws IOException {
        BufferedWriter writer = new BufferedWriter(
                new OutputStreamWriter(socket.getOutputStream(), "UTF-8")
        );
        writer.write("ACK\n");
        writer.flush(); // Send the the ACK signal which regulates message flow and reduces de-sync with the server.
    }

    public String receive() throws IOException {
        BufferedReader reader = new BufferedReader(
                new InputStreamReader(socket.getInputStream(), "UTF-8")
        );
        // Reads the UTF-8 message from the server and returns it.
        return reader.readLine();
    }

    public void close() {
        try {
            if (socket != null) socket.close();
        } catch (IOException ignored) {} // Just closes the socket connection
    }

    public static boolean dum_term(String data, TcpClient client) throws IOException {
        Scanner scn = new Scanner(System.in); // Cli Input keyboard input scan

        String[] Packet = data.split("\\|");
        String UserInput = null;
        String Mode = Packet[0]; // Splits the incoming packet into mode and data section

        switch (Mode) {
            case "0": // Print
                System.out.println(Packet[1]);

                return true;


            case "1": // Input
                System.out.print(Packet[1]);
                UserInput = scn.nextLine();
                if (Objects.equals(UserInput, "")) {
                    UserInput = "None";
                }
                client.send(UserInput);
                return true;


            case "2": // Close
                System.out.println(Packet[1]);

                return false;

            case "3": // Clear screen
                System.out.print("\033[H\033[2J");
                System.out.flush();

                return true;

            case "4": // blankline
                System.out.println(" ");

                return true;

            case "5": // Legacy support for password
                System.out.print(Packet[1]);
                UserInput = scn.nextLine();
                if (Objects.equals(UserInput, "")) {
                    UserInput = "None";
                }
                client.send(UserInput);
                return true;
            case "6": // Client Version
                client.send("TelePy-Java-1.9");
                return true;
            // No weather support for mode 7
            case "8": // temp fix for hidden input which is not working to using the general input
                System.out.print(Packet[1]);
                UserInput = scn.nextLine();
                if (Objects.equals(UserInput, "")) {
                    UserInput = "None";
                }
                client.send(UserInput);
                return true;

            // Modes 9-16
            // In depth documention is in the TelePy Documentation Version 1.9 section of the report
            default: // Print the packet if the mode is invalid for debugging
                System.out.println(Arrays.toString(Packet));
                client.send("ACK");
                return true;


        }


    }

    public static void main(String[] args) {
        Scanner scn = new Scanner(System.in);
        System.out.print("Server Ip :>>");
        String ip = scn.nextLine();
        if (Objects.equals(ip, "@")) { // Quick way of doing the local ip
            ip = "127.0.0.1";
        }
        TcpClient client = new TcpClient(ip, 1998);
        boolean Status = true;
        try {
            client.connect();

            client.send("terminal"); // Set the communication mode to terminal

            while (Status) {
                String response = client.receive();
                client.ack();
                Status = dum_term(response, client); // When the client disconnects or switches this returns false to break out of and exit cleanly.
            }

            client.close();
        } catch (IOException e) {
            e.printStackTrace(); // Prints the errors
        }
    }
}
