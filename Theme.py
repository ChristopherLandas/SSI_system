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

    Test_Color_Red = 'red'
    Test_Color_Blue = 'blue'
    Test_Color_Yellow = 'yellow'
    Test_Color_Green = 'green'
#TEST ONLY
#region icons
class Icons:
    
    info_icon = ctk.CTkImage(light_image= Image.open("image/info.png"), size=(22,22))
    notif_icon = ctk.CTkImage(light_image= Image.open("image/notification.png"), size=(30,30))
    display_setting_icon = ctk.CTkImage(light_image= Image.open("image/display_setting.png"), size=(30,30))
    delete_one_icon = ctk.CTkImage(light_image= Image.open("image/delete.png"), size=(25,25))
    delete_all_icon = ctk.CTkImage(light_image= Image.open("image/delete_all.png"), size=(25,25))
    #newly added 10.27.2023
    acc_icon = ctk.CTkImage(light_image=Image.open("image/acc.png"),size=(40,40))
    accounts_icon = ctk.CTkImage(light_image=Image.open("image/accounts.png"), size=(24,24))
    add_item_icon = ctk.CTkImage(light_image=Image.open("image/add_item.png"), size=(25,25))
    admin_icon = ctk.CTkImage(light_image=Image.open("image/admin.png"), size=(27,27))
    calendar_icon = ctk.CTkImage(light_image=Image.open("image/calendar.png"), size=(20,20))
    camera_icon = ctk.CTkImage(light_image=Image.open("image/camera.png"), size=(25,25))
    cat_icon = ctk.CTkImage(light_image=Image.open("image/cat.png"), size=(25,25))
    close = ctk.CTkImage(light_image=Image.open("image/close.png"),size=(16,16))
    account_creation_icon = ctk.CTkImage(light_image = Image.open("image/create_acc.png"), size=(24,24))
    dark_mode_icon = ctk.CTkImage(light_image=Image.open("image/dark_mode.png"), size=(25,25))
    dashboard_icon = ctk.CTkImage(light_image=Image.open("image/dashboard.png"),size=(22,22))
    deactivated_icon = ctk.CTkImage(light_image = Image.open("image/deact.png"), size=(24,24))
    edit_icon = ctk.CTkImage(light_image=Image.open("image/edit_icon.png"), size=(18,18))
    folder_icon = ctk.CTkImage(light_image=Image.open("image/folder.png"), size=(25,25))
    generate_report_icon = ctk.CTkImage(light_image=Image.open("image/gen_report.png"),size=(26,26))
    green_circle = ctk.CTkImage(light_image=Image.open("image/green_circle.png"), size=(25,25))
    hide_icon = ctk.CTkImage(light_image=Image.open("image/hide.png"), size=(25,25))
    histlogs_icon = ctk.CTkImage(light_image=Image.open("image/histlogs.png"),size=(22,25))
    info_icon = ctk.CTkImage(light_image= Image.open("image/info.png"), size=(36,36))
    inventory_icon = ctk.CTkImage(light_image=Image.open("image/inventory.png"),size=(24,25))
    logo_icon = ctk.CTkImage(light_image=Image.open("image/logo.png"),size=(24,25))
    inv_logo = ctk.CTkImage(light_image=Image.open("image/logo1.png"),size=(37,35))
    new_record_icon = ctk.CTkImage(light_image=Image.open("image/new_record.png"),size=(25,25))
    notif_icon = ctk.CTkImage(light_image=Image.open("image/notif.png"),size=(22,25))
    notification_icon = ctk.CTkImage(light_image=Image.open("image/notification.png"),size=(25,25))
    pass_icon = ctk.CTkImage(light_image=Image.open("image/pass_icon.png"),size=(22,25))
    patient_icon = ctk.CTkImage(light_image=Image.open("image/patient_icon.png"),size=(22,25))
    action = ctk.CTkImage(light_image=Image.open("image/patient.png"), size=(18,21))
    payment_icon = ctk.CTkImage(light_image=Image.open("image/payment_cash.png"), size=(25,25))
    person_icon = ctk.CTkImage(light_image=Image.open("image/person_icon.png"), size=(25,25))
    pholder_icon = ctk.CTkImage(light_image=Image.open("image/pholder.png"), size=(25,25))
    plus_icon = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(12,13))
    add_icon = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(13,13))
    view_icon = ctk.CTkImage(light_image=Image.open("image/receipt_icon.png"), size=(25,25))
    refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))
    report_icon = ctk.CTkImage(light_image=Image.open("image/report.png"),size=(22,22))
    restock_icon = ctk.CTkImage(light_image=Image.open("image/restock_plus.png"), size=(20,18))
    proceed_icon = ctk.CTkImage(light_image=Image.open("image/rightarrow.png"), size=(15,15))
    roles_icon = ctk.CTkImage(light_image = Image.open("image/role.png"), size=(24,24))
    sales_history_icon = ctk.CTkImage(light_image=Image.open("image/sales_history.png"), size=(25,25))
    sales_report_icon = ctk.CTkImage(light_image=Image.open("image/sales_report.png"), size=(16,16))
    sales_icon = ctk.CTkImage(light_image=Image.open("image/sales.png"),size=(26,20))
    save_icon = ctk.CTkImage(light_image=Image.open("image/save.png"), size=(25,25))
    schedule_icon = ctk.CTkImage(light_image=Image.open("image/schedule.png"), size=(25,25))
    screen_icon = ctk.CTkImage(light_image=Image.open("image/screen.png"), size=(25,25))
    search_icon = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(16,15))
    services_icon = ctk.CTkImage(light_image=Image.open("image/services.png"),size=(24,26))
    settings_icon = ctk.CTkImage(light_image=Image.open("image/setting.png"),size=(25,25))
    show_icon = ctk.CTkImage(light_image=Image.open("image/show.png"), size=(25,25))
    disposal_icon = ctk.CTkImage(light_image = Image.open("image/stock_sub.png"), size=(20,18))
    supplier_icon_ = ctk.CTkImage(light_image= Image.open("image/supplier.png"), size=(26,26))
    transact_icon = ctk.CTkImage(light_image=Image.open("image/transact.png"),size=(22,20))
    trash_icon = ctk.CTkImage(light_image= Image.open("image/trash.png"), size=(25,25))
    user_icon = ctk.CTkImage(light_image= Image.open("image/user_icon.png"), size=(25,25))
    user_setting_icon = ctk.CTkImage(light_image=Image.open("image/usersetting.png"),size=(24,27))
    view_icon = ctk.CTkImage(light_image= Image.open("image/view.png"), size=(25,25))
    
#endregion
    
    zoom_in_icon = ctk.CTkImage(light_image= Image.open("image/zoomin.png"), size=(25,25))
    zoom_out_icon = ctk.CTkImage(light_image= Image.open("image/zoomout.png"), size=(25,25))
    zoom_reset_icon = ctk.CTkImage(light_image= Image.open("image/zoomreset.png"), size=(25,25))

    admin_user_icon = ctk.CTkImage(light_image= Image.open("image/admin_icon.png"), size=(35,35))
    other_user_icon = ctk.CTkImage(light_image= Image.open("image/other_icon.png"), size=(35,35))
   
