#include <WiFi.h>
#include <WebServer.h>
#include <esp32cam.h>

const char* ssid = "Lee";
const char* password = "66765621";

WebServer server(80);
static auto hiRes = esp32cam::Resolution::find(800, 600);

int gpLb = 12; // Left 1
int gpLf = 13; // Left 2
int gpRb = 15; // Right 1
int gpRf = 14; // Right 2

void setup() {
  Serial.begin(115200);

  { // Motor settings
    pinMode(gpLb, OUTPUT);
    pinMode(gpLf, OUTPUT);
    pinMode(gpRb, OUTPUT);
    pinMode(gpRf, OUTPUT);
    
    digitalWrite(gpLb, LOW);
    digitalWrite(gpLf, LOW);
    digitalWrite(gpRb, LOW);
    digitalWrite(gpRf, LOW);
  }
  
  { // Camera settings
    using namespace esp32cam;
    Config cfg;
    cfg.setPins(pins::AiThinker);
    cfg.setResolution(hiRes);
    cfg.setBufferCount(2);
    cfg.setJpeg(80);

    bool ok = Camera.begin(cfg);
    Serial.println(ok ? "CAMERA OK" : "CAMERA FAIL");
  }

  WiFi.persistent(false);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  Serial.print("http://");
  Serial.println(WiFi.localIP());
  
  server.on("/cam-hi.jpg", handleJpg);
  server.on("/", handleOnConnect);
  server.on("/go", handleGo);
  server.on("/back", handleBack);
  server.on("/right", handleRight);
  server.on("/left", handleLeft);
  server.on("/goone", handleGoOne);
  server.on("/backone", handleBackOne);
  server.on("/rightone", handleRightOne);
  server.on("/leftone", handleLeftOne);
  server.onNotFound(handleNotFound);
  
  server.begin();
  Serial.println("HTTP server started");
  
}

void loop() {
  server.handleClient();
}

void WheelAct(int nLf, int nLb, int nRf, int nRb)
{
  digitalWrite(gpLf, nLf);
  digitalWrite(gpLb, nLb);
  digitalWrite(gpRf, nRf);
  digitalWrite(gpRb, nRb);
}

void handleJpg()
{
  if (!esp32cam::Camera.changeResolution(hiRes)) {
    Serial.println("SET-HI-RES FAIL");
  }
  serveJpg();
}

void serveJpg()
{
  auto frame = esp32cam::capture();
  if (frame == nullptr) {
    Serial.println("CAPTURE FAIL");
    server.send(503, "", "");
    return;
  }
  Serial.printf("CAPTURE OK %dx%d %db\n", frame->getWidth(), frame->getHeight(),
                static_cast<int>(frame->size()));

  server.setContentLength(frame->size());
  server.send(200, "image/jpeg");
  WiFiClient client = server.client();
  frame->writeTo(client);
}

void handleOnConnect() {
  Serial.println("Server start");
  server.send(200, "text/html", "Server start");
  WheelAct(LOW, LOW, LOW, LOW); 
}

void handleGo() {
  WheelAct(HIGH, LOW, LOW, HIGH);
  delay(10);
  WheelAct(LOW, LOW, LOW, LOW);
  Serial.println("Go");
  server.send(200, "text/html", "Go"); 
}

void handleBack() {
  WheelAct(LOW, HIGH, HIGH, LOW);
  delay(10);
  WheelAct(LOW, LOW, LOW, LOW);
  Serial.println("Back");
  server.send(200, "text/html", "Back"); 
}

void handleRight() {
  WheelAct(HIGH, LOW, HIGH, LOW); 
  delay(10);
  WheelAct(LOW, LOW, LOW, LOW);
  Serial.println("Right");
  server.send(200, "text/html", "Right");
}

void handleLeft() {
  WheelAct(LOW, HIGH, LOW, HIGH);
  delay(10);
  WheelAct(LOW, LOW, LOW, LOW);
  Serial.println("Left");
  server.send(200, "text/html", "Left"); 
}

void handleGoOne() {
  WheelAct(HIGH, LOW, LOW, HIGH);
  delay(290);
  WheelAct(LOW, LOW, LOW, LOW);
  Serial.println("GoOne");
  server.send(200, "text/html", "GoOne"); 
}

void handleBackOne() {
  WheelAct(LOW, HIGH, HIGH, LOW);
  delay(290);
  WheelAct(LOW, LOW, LOW, LOW);
  Serial.println("BackOne");
  server.send(200, "text/html", "BackOne"); 
}

void handleRightOne() {
  WheelAct(HIGH, LOW, HIGH, LOW); 
  delay(210);
  WheelAct(LOW, LOW, LOW, LOW);
  Serial.println("RightOne");
  server.send(200, "text/html", "RightOne");
}

void handleLeftOne() {
  WheelAct(LOW, HIGH, LOW, HIGH);
  delay(250 );
  WheelAct(LOW, LOW, LOW, LOW);
  Serial.println("LeftOne");
  server.send(200, "text/html", "LeftOne"); 
}

void handleNotFound(){
  server.send(404, "text/plain", "Not found");
}
