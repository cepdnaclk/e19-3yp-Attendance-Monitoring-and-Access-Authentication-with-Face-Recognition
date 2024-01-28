# FACE-SECURE

## Attendance Management System with Face Recognition

---

![](docs/images/facerecog.png)

Our project redefines access control through a blend of facial recognition, fingerprint scanning, and PIN authentication. By integrating these three authentication methods, we create a robust yet user-friendly security system.

Facial recognition offers seamless, contactless access, while fingerprint scanning adds a layer of precision and uniqueness. For familiarity, a PIN entry option is also available.

This multi-factor approach prioritizes security without compromising user convenience. Our vision is to provide organizations with a dynamic, impenetrable security solution that adapts to diverse user preferences.

Join us as we revolutionize access security, empowering organizations with a flexible and fortified system for safeguarding their premises.

## Team & ePortfolio

| Registration Number | Name             | Email                | Profile Link                                    |
| ------------------- | ---------------- | -------------------- | ----------------------------------------------- |
| E/19/278            | Tharudi Perera   | e19278@eng.pdn.ac.lk | [Tharudi Perera](https://www.thecn.com/TP993)   |
| E/19/295            | Janitha Dilshan  | e19295@eng.pdn.ac.lk | [Janitha Dilshan](https://www.thecn.com/JD1243) |
| E/19/300            | Asela Hemantha   | e19300@eng.pdn.ac.lk | [Asela Hemantha](https://www.thecn.com/LP990)   |
| E/19/452            | Ashan Wimalasiri | e19452@eng.pdn.ac.lk | [Ashan Wimalasiri](https://www.thecn.com/PW491) |
| E/19/492            | Nuwantha Lakshan | e19492@eng.pdn.ac.lk | [Nuwantha Lakshan](https://www.thecn.com/NL856) |

## 1.Problem Overview

Deficiencies of Manual Attendance Management System​

- Time-Consuming Process​
- Prone to Errors​
- Lack of Real-Time Data​
- Bureaucratic Hassles​
- Limited Scalability​
- Security Concerns​

## 2.Why is this need?

- Efficiency in Tracking With Face Detection​
- Multi Security Levels​
- Error Reduction​
- Real-Time Updates​
- Streamlined Administration​
- Scalability​
- Enhanced Security

## 3.Solution Architecture

- ### High-Level Overview

  Out attendance management System has 3 tiers

- Attendance Management Device
- Backend Server
- Frontend Dashboards (User & Admin)
- ### Roles of the System

### 1.Admin

Admin can add and remove employees
See the employee details (image, name, absent date)
Unauthorized person entering alert (optional)

To access the admin dashboard

Should have a current date attendance tracked by face detection
Fingerprint access or keypad

### 2. Employees

Attendance marks either face detection or fingerprint
They have their profile to see their attendance


- ### Control Flow of the System
  ![](docs/images/1.png)
- ### Data Flow of the System
  ![](docs/images/2.png)

## 4.Infrastructure

- ### Technology Stack

  ![](docs/images/4.png)

- ### Hardware Components
  ![](docs/images/3.png)

## 5.BOM

|    Component                |       Quantity​   |     Unit Price (LKR)​ | Cost (LKR)​                                      |
| ----------------------------| ---------------- | -------------------- | ----------------------------------------------- |
| Raspberry Pi​ 3 Board        |         1        |      21,650          |              21,650                             |
| Rasberry Pi Camera Module​ 3 |         1        |       1,370          |               1,370                             | 
| R307 Fingerprint Sensor​     |         1        |       3,600          |               3,600                             |
| Keypad​                      |         1        |         150          |                 150                             |
| Solenoid door lock          |         1        |       1,240          |               1,240                             |
| LCD Touch Screen            |         1        |      13,850          |              13,850                             |
| PIR Sensor Module           |         1        |         250          |                 250                             |
| Jumper Wires                |        20        |          10          |                 200                             |
|Total Cost                   |                  |                      |              46,170                             |

## 6.Components

- Raspberry Pi 3 Board​
- Raspberry Pi Camera Module 3​
- RE307 Fingerprint Sensor
- Keypad
- Solenoid Door Lock
- PIR Sensor Module 
  
## 7.Extendibility & Scalability

- Integration with Other Systems​
- Advanced Reporting Modules​
- Accurate & consistent performance
- Power switching mode
- Error Handling
- Easily scalable

## 8.For More Details
[Our Project Page](https://cepdnaclk.github.io/e19-3yp-Attendance-Monitoring-and-Access-Authentication-with-Face-Recognition/)
[Our Git Repository](https://github.com/cepdnaclk/e19-3yp-Attendance-Monitoringand-Access-Authentication-with-Face-Recognition)
[Department of Computer Engineering](https://www.ce.pdn.ac.lk/)
[University of Peradeniya](https://eng.pdn.ac.lk/)
