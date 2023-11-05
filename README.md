# Vehicle Project README

## Introduction

In the making of the vehicle, we encountered many challenges that we eventually overcame. One of those challenges was the design itself. We had numerous source materials to base our project on, but we decided to innovate. We took two aluminum plates from a Tetrix kit and a motor. After we had the base, our team started a trial and error process in which we decided on our current design. The design adheres to all of the requirements of the WRO.

## Mechanical Design

When the base was completed, we started to create the front of the vehicle and all of the mechanical aspects of the steering mechanism. We designed it in SolidWorks with the help of a partner. We gave him the instructions and he assisted us with the technical aspects of using SolidWorks. Along the way, we encountered a problem with the inner workings of the steering mechanism. The issue was that the servo motor shaft was off the original position. While not immediately noticeable, we brainstormed and quickly resolved it. In the end, we sent all of the pieces to a slicer and to a 3D printer to be made.

## Construction and Adaptations

After the pieces arrived, we began the construction of the vehicle. As we progressed, we made some adjustments and changes in the design to accommodate newer parts like the motor. The motor had a shaft of 6mm, while our pulley connector was 4mm in diameter, making them incompatible. However, we were able to create an adapter using aluminum pieces that remained from the Tetrix kit.

## Software and Hardware Integration

At this point, we were simultaneously working on the software and hardware, making clear the requirements for each part and communicating any modifications that could affect either side.

## Platform Decision

We initially planned to create an Arduino white driver / Raspberry Pi hybrid, using the Arduino as a motor driver with connections to the Raspberry Pi interface, which was supposed to process and recognize obstacles. However, in the end, we decided to use only a Raspberry Pi, motor driver, and a camera. This streamlined the programming process as it was focused on a single platform.

## Power Management

To address power compatibility, we installed the motor driver's power IN into the battery and then the control pins into the Raspberry Pi. However, the Raspberry Pi can only be powered by 5 volts, not 12 volts. To overcome this, we first created a voltage regulator to reduce the output to the Raspberry Pi. After initial testing, we later purchased a more powerful and precise regulator.

## Adding Vision

With the energy source issue resolved, we needed to equip the vehicle with "eyes" - a webcam. We modified it to be more compact and easy to work with.

## Completion and Reflection

In the end, this machine was finally completed with the help of many people and a team that was united, with each member specializing in their field of knowledge but also being open to help in any way possible. This journey has led us to expand our minds and inspire us to keep pursuing what we love. We presented this project to many people, including other members of the university and even to companies like Samsung DR. However, the people who remain the most impressed by it are us, the creators: Angel Veloz, Eudy Moreno, and Ruben Martinez. We never believed that in less than one and a half months in the university, we would be creating this vehicle, and we appreciate everything. Our journey has only just begun.

## Team Information

**Names:** Angel Veloz, Eudy Moreno, Ruben Martinez

**University:** PUCMM (Pontificia Universidad Católica Madre y Maestra), Dominican Republic

**Program:** Mechatronic Engineering

## Acknowledgements

We would like to express our gratitude to the specialists in the University, including the professor of advanced Robotics, and many of the seniors who provided us with invaluable help and guidance throughout our journey.
