import customtkinter as ctk
from PIL import Image
import screeninfo
[print(screen) for screen in screeninfo.get_monitors()]
class Color:
    White_Lotion = "#FCFCFC"
    White_Milk = "#FFFDF6"
    White_Platinum = "#E5E5E5"
    White_Ghost = "#F9F9F9"
    White_Gray = "#EFEFEF"
    White_Chinese = "#E0E0E0"
    White_AntiFlash = "#F1F1F1"
    White_SilverSand = "#C5C5C5"

    White_Color = ("#FCFCFC","#FFFDF6","#E5E5E5","#F9F9F9","#EFEFEF","#E0E0E0","#F1F1F1","#C5C5C5","#B9B9B9")
    
    Blue_Oxford = "#0A2647"
    Blue_Maastricht = "#06283D"
    Blue_Cobalt = "#205295"
    Blue_Yale = "#0D5794"
    Blue_Steel = "#2C74B3"
    Blue_Tufts = "#3B8ED0"
    
    Blue_LapisLazuli = "#296FA7"
    Blue_LapisLazuli_1 = "#296AA3"

    Grey_Bright_2 = "#EBEBEB"
    Grey_Davy = "#5D5D5D"
    Grey_Bright = "#EEEEEE"
    
    Platinum = "#E7E7E7"
    Light_Green = "#97DC86"
    
    Red_Tulip = "#FD8A8A"
    Red_Pastel = "#FF6464"
    Red_Hover = "#D45353"
    
    Green_Pistachio = "#83BD75"
    Green_Aparagus = "#6E9D62"
    
    Orange_Dandelion = "#FFD966"
    

    White_Color = ("#FCFCFC","#FFFDF6","#E5E5E5","#F9F9F9","#EFEFEF","#E0E0E0","#F1F1F1","#C5C5C5",)
    Red_Color = ("#FD8A8A","#FF6464","#EB455F","#E6556B" )
    
    Safe_color =  "#97DC86" #"green"
    Reorder_Color = "#FFE569"  #"yellow"
    Critical_Color = "#FFBB5C" #"#FFA559"
    Out_Stock_Color = "#A8A196"  #"#413F42"
    Near_Expire_Color = "#FFA559" #"#FF9B50"
    Expire_Color = "#FD8A8A" #"#E74646"
    
    Hover_Safe_color =  "#85D671" #"green"
    Hover_Reorder_Color = "#FFE047"  #"yellow"
    Hover_Critical_Color = "#FFAA33" #"#FFA559"
    Hover_Out_Stock_Color = "#999185"  #"#413F42"
    Hover_Near_Expire_Color = "#FF8F33" #"#FF9B50"
    Hover_Expire_Color = "#FD7272" #"#E74646"

#TEST ONLY
class Icons:
    
    info_icon = ctk.CTkImage(light_image= Image.open("image/info.png"), size=(22,22))
    notif_icon = ctk.CTkImage(light_image= Image.open("image/notification.png"), size=(30,30))
    display_setting_icon = ctk.CTkImage(light_image= Image.open("image/display_setting.png"), size=(30,30))
    delete_one_icon = ctk.CTkImage(light_image= Image.open("image/delete.png"), size=(25,25))
    delete_all_icon = ctk.CTkImage(light_image= Image.open("image/delete_all.png"), size=(25,25))
    
   
