---
title: "System Architektur Spezifikation"
version: 0.1

keywords: [THAB, Informatik IV, 3D-Bionics]

---

# System Architektur Überblick

## Hardware-Software Verbund

### Zusammenhang des Systems

```mermaid
flowchart LR

Kontroll-Software <-->| Serial|Arduino <-->|Serial| Servo-Driver

Buttons --> Arduino

Servo-Driver .->|PWM| a(Servo 1) & b(Servo 2) & c(Servo 3) & d(Servo 4) & e(Servo 5)
```

### Erklärung

Die Kontrollsoftware sendet über eine serielle-Schnittstelle Datenpakete an den Arduino, welcher die einzelnen Servo-Motoren über einen externen Servo-Driver ansteuert. 

Der Arduino (und damit die Servos) kann theoretisch auch über Buttons welche direkt an den Arduino angeschlossen sind angesteuert werden. In diesem Fall gibt der Arduino lediglich die neuen Positions-Werte der Finger an die Kontroll-App zurück.
