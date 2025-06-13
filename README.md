<img src="https://raw.githubusercontent.com/gbit-is/hyperdome/refs/heads/main/misc/hyperdome_logo_export_blue.svg" alt="logo" width="200"/>

R2-D2 Dome lighting solution using off the shelf components

# Features
- no custom PCB's
- individual on/off controls for RLD/FLD
- Full RGB control for PSI's and Holos

# Things I wanna add
- The option to control the lights via serial commands
- redesign the RLD/FLD to use RGB led matrices 
- Add Servo controls
  
# Compatability
This is designed to be compatible with the V4, R2D2 Dome by [mrbaddeley](https://www.patreon.com/c/mrbaddeley). It might work with other domes but I won't be testing them

# BOM

| Component | qt | image | 
| --------- | -- | ----- | 
| Pi Pico   | 1  | <img src="https://raw.githubusercontent.com/gbit-is/hyperdome/refs/heads/main/misc/pi_pico.jpeg" alt="logo" width="200"/> |
| Max7219 green | 1 |<img src="https://raw.githubusercontent.com/gbit-is/hyperdome/refs/heads/main/misc/max7219.jpg" alt="max7219" width="200"/> |
| Max7219 blue | 1 | <img src="https://raw.githubusercontent.com/gbit-is/hyperdome/refs/heads/main/misc/max7219.jpg" alt="max7219" width="200"/>|
| 8 LED Neopixel ring | 5 | <img src="https://raw.githubusercontent.com/gbit-is/hyperdome/refs/heads/main/misc/neopixel_ring.jpeg" alt="neopixel_ring" width="200"/> |
| 3mm fiber optic cable | 5 meters | <img src="https://raw.githubusercontent.com/gbit-is/hyperdome/refs/heads/main/misc/fiber_cable.webp" alt="fiber_cable" width="200"/> |

# Print list:
| File | qt |
| ---- | -- |
| FLD/fld_max_mount.stl | 1 |
| RLD/rld_fiber_mount.stl | 1 |
| RLD/rld_mount_max.stl | 1 |
| RLD/rld_spacer.stl | 2 |
| PSI/large_psi.stl | 1 |
| PSI/small_psi.stl | 1 |
| HOLO/holo_mount.stl | 3 |
| HOLO/holo_lens_cover.stl | 3 |

# Assembly

Tools:
- box cutter/hobby knife (with a new, sharp blade)
- Glue
- 3mm drill, 3.2mm drill 

I will make a proper guide for assembly, note that some parts are deliberately very tight and might need some minor modifications to work properly.  

If the holes for the fiber optic cable isn't snug it will just come loose, so a tight fit is required. if you can't get the fiber optic through a hole, I recomend using a handheld hobby drill with a 3mm bit and re-boring the hole, if it still doesn't work, then use a 3.2mm bit 

the "rld spacer" is un purpose slightly oversized, instead of fine tuning it to my printer and fileament I just left it slightly oversized and used a hobby knife to resize the contact points to a point where they can be friction fitted.
