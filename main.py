from functools import wraps
import os
import tkinter as tk
from tkinter import messagebox,filedialog,ttk
from ft import facebookFill
import file_control as fc

'''
变量规则: 类型缩写_名称
类型列表：
l:Label,tk的标签, 文本标签
lf:LabelFrame, tk的带标签的窗体
cb:combobox, ttk的下拉控件
b:Button
list:就是list
e:Entry, tk的输入框
'''


class MyGUI:

#-------------------------这里是装饰器-----------------------------------
    def dec_check_ads_data_status(func):
        def filestatus(filename):
            return os.stat(filename).st_size != 0 and os.path.exists(filename)

        @wraps(func)
        def return_func(*args, **kwargs):
            status = 'OK'
            color='green'
            obj_gui = args[0]
            files=[obj_gui.workpath+'title.txt',obj_gui.workpath+'price.txt',obj_gui.workpath+'desc.txt',obj_gui.workpath+'tags.txt',obj_gui.workpath+'cate.txt']
            for file in files:
                if not filestatus(file):
                    status = 'Not OK'
                    color='red'
                    break
            obj_gui.l_status_indicator.config(text="Current status:"+status,fg=color)
            func(*args, **kwargs)
        return return_func
    
    def dec_check_ads_data_status_init(func):
        def filestatus(filename):
            return os.stat(filename).st_size != 0 and os.path.exists(filename)

        @wraps(func)
        def return_func(*args, **kwargs):
            func(*args, **kwargs)
            status = 'OK'
            color='green'
            obj_gui = args[0]
            files=[obj_gui.workpath+'title.txt',obj_gui.workpath+'price.txt',obj_gui.workpath+'desc.txt',obj_gui.workpath+'tags.txt',obj_gui.workpath+'cate.txt']
            for file in files:
                if not filestatus(file):
                    status = 'Not OK'
                    color='red'
                    break
            obj_gui.l_status_indicator.config(text="Current status:"+status,fg=color)
        return return_func

#-----------------------------------初始化函数------------------------------
    @dec_check_ads_data_status_init
    def __init__(self, master):
        #依赖文件和文件夹的初始化，不遵循命名规则了
        #UI中的全局变量定义
        self.profile_rootpath = "./Profiles/"
        self.adsdata_rootpath = "./AdsData/"
        self.workpath = "./AdsData/Default/"
        self.workprofile = os.path.abspath("./Profiles/Default")

        directoryList=["./AdsData/","./AdsData/Default/","./Assert/","./Assert/ico/","./Profiles/","./Profiles/Default/","./Driver/"]
        fileList=["title.txt","price.txt","desc.txt","cate.txt","tags.txt"]
        fileList = list(map(lambda x:self.workpath+x,fileList))
        fc.DirFile_creation(directoryList,fileList)

        #操作界面生成
        self.master = master
        master.title("Facebook Semi-auto Fill Tool")

        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

        #下半部分界面，状态栏，用于指示工作区内的广告信息是否合法
        self.lf_ads_status = tk.LabelFrame(master,text='Ads Status')
        self.lf_ads_status.pack(side="bottom",padx=5,pady=5,fill="x")
        
        self.l_status_indicator = tk.Label(self.lf_ads_status,text="Current status:")
        self.l_status_indicator.pack(side="top",padx=5)

        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

        #左半边界面，用于控制广告的文案
        self.lf_ads_setting = tk.LabelFrame(master,text='Ads Setting')
        self.lf_ads_setting.pack(side="bottom",padx=5,pady=5,fill="x")

        #广告ads载入frame
        self.f_advertising = tk.Frame(self.lf_ads_setting)
        self.f_advertising.pack(padx=5,pady=2,fill="x")
        #所选广告说明
        self.l_ads_indicator = tk.Label(self.f_advertising,text="Current Ads:")
        self.l_ads_indicator.pack(side="left",padx=2,pady=5)
        #下拉选单
        self.list_adsdata=fc.show_dir(self.adsdata_rootpath)
        self.cb_adsdata = ttk.Combobox(self.f_advertising,values=self.list_adsdata,state='readonly',width=12)
        self.cb_adsdata.pack(side="left",pady=2)
        self.cb_adsdata.set('Default')
        #添加
        self.b_Add_ads = tk.Button(self.f_advertising, text="+", width=1,height=1)
        self.b_Add_ads.pack(side="left",padx=1,pady=5)
        #删除
        self.b_Remove_ads = tk.Button(self.f_advertising, text="-", width=1,height=1)
        self.b_Remove_ads.pack(side="left",padx=1,pady=5)

        #管理广告文案
        self.b_Check_ads_detail = tk.Button(self.lf_ads_setting, text="Manage Ads Data", width=10)
        self.b_Check_ads_detail.pack(padx=5,pady=5,side="top",fill="x")

        # self.b_test1 = tk.Button(self.lf_ads_setting, text="D", width=10,command=lambda : self.cb_adsdata.set('Default'))
        # self.b_test1.pack(padx=5,pady=2,side="top",fill="x")

        # self.b_test2 = tk.Button(self.lf_ads_setting, text="SS", width=10,command=lambda :self.cb_adsdata.set('SS'))
        # self.b_test2.pack(padx=5,pady=2,side="top",fill="x")


        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

        #右半边界面，用于控制浏览器
        self.lf_main_area = tk.LabelFrame(master,text='Main')
        self.lf_main_area.pack(side="left",padx=5,pady=5,fill="y")

        #profile载入frame
        self.f_profile = tk.Frame(self.lf_main_area)
        self.f_profile.pack(padx=5,pady=2,fill="x")
        #区域说明
        self.l_profile_indicator = tk.Label(self.f_profile,text="Current profile:")
        self.l_profile_indicator.pack(side="left",padx=2,pady=5)
        #下拉浏览器Profile选单
        self.list_profile=fc.show_dir(self.profile_rootpath)
        self.cb_profiles = ttk.Combobox(self.f_profile,values=self.list_profile,state='readonly',width=12)
        self.cb_profiles.pack(side="left",pady=2)
        self.cb_profiles.set('Default')
        #添加浏览器Profile
        self.b_Add_profile = tk.Button(self.f_profile, text="+", width=1,height=1)
        self.b_Add_profile.pack(side="left",padx=1,pady=5)
        #删除浏览器Profile
        self.b_Remove_profile = tk.Button(self.f_profile, text="-", width=1,height=1)
        self.b_Remove_profile.pack(side="left",padx=1,pady=5)

        #启动按钮
        self.b_Launch = tk.Button(self.lf_main_area, text="Launch Browser", width=20)
        self.b_Launch.pack(padx=5,pady=5,fill="x")

        #输入广告按钮
        self.b_Fill_form = tk.Button(self.lf_main_area, text="Fill Form", width=20)
        self.b_Fill_form.pack(padx=5,pady=5,fill="x")

        #群发group的时候的按钮
        self.b_Select_group = tk.Button(self.lf_main_area, text="List More Place", width=20)
        self.b_Select_group.pack(padx=5,pady=5,fill="x")

        #更新本条广告按钮
        self.b_Update_ads = tk.Button(self.lf_main_area, text="Change Current Ads", width=20)
        self.b_Update_ads.pack(padx=5,pady=5,fill="x")

        #更新本条广告按钮(页面版)
        self.b_Update_ads_page = tk.Button(self.lf_main_area, text="Change Ads Page", width=20)
        self.b_Update_ads_page.pack(padx=5,pady=5,fill="x")


        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

        #Ads区域按键事件绑定
        self.cb_adsdata.bind("<<ComboboxSelected>>",self._event_ads_data_select)
        self.b_Add_ads.configure(command=self._event_add_ads)
        self.b_Remove_ads.configure(command=self._event_remove_ads)
        self.b_Check_ads_detail.configure(command=self._event_manage_ads)


        #Main区域按键事件绑定
        self.cb_profiles.bind("<<ComboboxSelected>>",self._event_cb_profile)
        self.b_Add_profile.configure(command=self._event_add_profile)
        self.b_Remove_profile.configure(command=self._event_remove_profile)
        self.b_Launch.configure(command=self._event_launch)
        self.b_Fill_form.configure(command=self._event_fill_form)
        self.b_Select_group.configure(command=self._event_select_group)
        self.b_Update_ads.configure(command=self._event_update_ads)
        self.b_Update_ads_page.configure(command=self._event_update_ads_page)

#---------------------------------事件函数区域-------------------------------------------
    #-----左半边事件函数-----
    @dec_check_ads_data_status_init
    def _event_ads_data_select(self,event):
        #切换了广告文案下拉框的选项后，触发这个函数，将载入的广告文案文件夹变更到所选文件夹
        self.workpath = self.adsdata_rootpath + self.cb_adsdata.get() + '/'
    
    @dec_check_ads_data_status_init
    def _event_add_ads(self):
        self.sub_window = tk.Toplevel(self.master)
        self.sub_window.title('Add Ads Data')

        self.e_new_adsdata_name = tk.Entry(self.sub_window)
        self.e_new_adsdata_name.pack(side='left',padx=5,pady=5,fill="y")

        self.b_Add_ads_subwindow = tk.Button(self.sub_window, text="Add", width=10, command=self._event_add_ads_subwindow)
        self.b_Add_ads_subwindow.pack(side='left',padx=5,pady=5,fill="y")

        self.sub_window.focus_force()

    def _event_add_ads_subwindow(self):
        adsdata_name = self.e_new_adsdata_name.get()
        adsdata_path = self.adsdata_rootpath+adsdata_name
        if fc.create_dir(adsdata_path):
            messagebox.showinfo('Success',message='Successfully added!')
            self.cb_adsdata['values']=fc.show_dir(self.adsdata_rootpath)
            self.workpath=adsdata_path+'/'
            fileList=["title.txt","price.txt","desc.txt","cate.txt","tags.txt"]
            fileList = list(map(lambda x:self.workpath+x,fileList))
            fc.DirFile_creation(file_list=fileList)
            AdsPage(self.master,self.workpath,adsdata_name,self.l_status_indicator)
            self.sub_window.destroy()



        else:
            messagebox.showerror('Error',message='Ads data has existed!')
            self.e_new_adsdata_name.delete(0,tk.END)
            self.sub_window.deiconify()

    @dec_check_ads_data_status_init
    def _event_remove_ads(self):
        response = messagebox.askquestion('Action Confirm',message='Do you want to delete this ads data?',)
        if response=='yes':
            if self.cb_adsdata.get()=='Default':
                messagebox.showerror('Error',message='Default ads data cannot be deleted!')
                return
            fc.removedir('./AdsData/'+self.cb_adsdata.get())
            self.cb_adsdata['values']=fc.show_dir(self.adsdata_rootpath)
            messagebox.showinfo('Success',message='Successfully deleted!')
            self.cb_adsdata.set('Default')
            self.workpath = self.adsdata_rootpath + 'Default/'
    
    @dec_check_ads_data_status_init
    def _event_manage_ads(self):
        #生成文案的预览和编辑页面
        ap = AdsPage(self.master,self.workpath,self.cb_adsdata.get(),self.l_status_indicator)
        print(ap)



    
    #-----右半边事件函数-----

    def _event_launch(self):
        try:
            try:
                self.facebook = facebookFill(self.workprofile)
            except:
                self.facebook = facebookFill(os.path.abspath("./Profiles/Default"))
            self.facebook.launchbrowser()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _event_fill_form(self):
        # Fill按钮点击事件的函数
        try:
            # 运行的代码
            self.facebook.set_folderpath(self.workpath)
            self.facebook.autofill()
        except Exception as e:
            # 出现错误时弹出错误提示框
            messagebox.showerror("Error", str(e))

    def _event_select_group(self):
        try:
            # 运行的代码
            self.facebook.autolist()
        except Exception as e:
            # 出现错误时弹出错误提示框
            messagebox.showerror("Error", str(e))

    def _event_update_ads(self):
        try:
            # 运行的代码
            self.facebook.set_folderpath(self.workpath)
            self.facebook.autoupdate()
        except Exception as e:
            # 出现错误时弹出错误提示框
            messagebox.showerror("Error", str(e))

    def _event_update_ads_page(self):
        try:
            # 运行的代码
            self.facebook.set_folderpath(self.workpath)
            self.facebook.autoupdatelink()
        except Exception as e:
            # 出现错误时弹出错误提示框
            messagebox.showerror("Error", str(e))

    def _event_cb_profile(self,event):
        selected_profile = self.cb_profiles.get()
        self.workprofile = os.path.abspath(self.profile_rootpath+selected_profile)
        print(self.workprofile)

    def _event_add_profile(self):      

        self.sub_window = tk.Toplevel(self.master)
        self.sub_window.title('Add Account Profile')

        self.e_new_profile_name = tk.Entry(self.sub_window)
        self.e_new_profile_name.pack(side='left',padx=5,pady=5,fill="y")

        self.b_Add_prof_subwindow = tk.Button(self.sub_window, text="Add", width=10, command=self._event_add_prof_subwindow)
        self.b_Add_prof_subwindow.pack(side='left',padx=5,pady=5,fill="y")

        self.sub_window.focus_force()
    
    def _event_add_prof_subwindow(self):
        profile_name = self.e_new_profile_name.get()
        profile_path = self.profile_rootpath+profile_name
        if fc.create_dir(profile_path):
            messagebox.showinfo('Success',message='Successfully added!')
            self.cb_profiles['values']=fc.show_dir(self.profile_rootpath)
            self.sub_window.destroy()
        else:
            messagebox.showerror('Error',message='Profile has existed!')
            self.e_new_profile_name.delete(0,tk.END)
            self.sub_window.deiconify()

    def _event_remove_profile(self):
        response = messagebox.askquestion('Action Confirm',message='Do you want to delete this profile?',)
        if response=='yes':
            if self.cb_profiles.get()=='Default':
                messagebox.showerror('Error',message='Default Profile cannot be deleted!')
                return
            fc.removedir('./Profiles/'+self.cb_profiles.get())
            self.cb_profiles['values']=fc.show_dir(self.profile_rootpath)
            messagebox.showinfo('Success',message='Successfully deleted!')
            self.cb_profiles.set('Default')

#-------------------------事件函数区域结束------------------------------------------------
    def _event_check_adsdata(self):
        pass

#--------------------------------Class Page----------------------------------------------
class AdsPage(MyGUI):
    def __init__(self, master, workpath,adsdata = 'Default',check_lable=object()):
        self.folderpath = workpath
        self.workpath = workpath
        self.check_lable = check_lable

        self.sub_ads_window = tk.Toplevel(master)
        self.sub_ads_window.title('Ads Data Title ：' + adsdata)

        self.price_cate_frame=tk.LabelFrame(self.sub_ads_window,text='Price and Category')
        self.price_cate_frame.pack(padx=5,pady=5,fill="x")
        self.price_indicator = tk.Label(self.price_cate_frame,text="Price: ")
        self.price_indicator.pack(padx=5,pady=5,fill="x",side='left')
        self.price_input = tk.Entry(self.price_cate_frame)
        self.price_input.pack(padx=5,pady=5,fill="x",side='left')
        self.cate_review = tk.StringVar()
        self.cate_combox = ttk.Combobox(self.price_cate_frame,textvariable=self.cate_review, values=['Tools','Miscellaneous','Garden'],state='readonly')
        self.__checkcategory(self.cate_combox)
        self.cate_combox.pack(padx=5,pady=5,fill="x",side='right')
        self.cate_indicator = tk.Label(self.price_cate_frame,text="Category: ")
        self.cate_indicator.pack(padx=5,pady=5,fill="x",side='right')

        self.title_frame = tk.LabelFrame(self.sub_ads_window,text='Title')
        self.title_frame.pack(padx=5,pady=5,fill="x")
        self.title_review = tk.Text(self.title_frame,width=100,height=3, autoseparators=True)
        self.title_review.pack(padx=5,pady=5,fill="x")
        self.title_import_btn = tk.Button(self.title_frame,text='Import', command=self._event_import(self.title_review,'title.txt'))
        self.title_import_btn.pack(padx=5, pady=5,anchor='e')

        self.desc_frame = tk.LabelFrame(self.sub_ads_window,text='Description')
        self.desc_frame.pack(padx=5,fill="x")
        self.desc_review = tk.Text(self.desc_frame,width=100, autoseparators=True)
        self.desc_review.pack(padx=5,pady=5,fill="x")
        self.desc_import_btn = tk.Button(self.desc_frame,text='Import', command=self._event_import(self.desc_review,'desc.txt'))
        self.desc_import_btn.pack(padx=5,pady=5, anchor='e')

        self.tags_frame = tk.LabelFrame(self.sub_ads_window,text='Tags')
        self.tags_frame.pack(padx=5,pady=5,fill="x")
        self.tags_review = tk.Text(self.tags_frame,width=100,height=3, autoseparators=True)
        self.tags_review.pack(padx=5,pady=5,fill="x")
        self.tags_import_btn = tk.Button(self.tags_frame,text='Import',command=self._event_import(self.tags_review,'tags.txt'))
        self.tags_import_btn.pack(padx=5,pady=5, anchor='e')

        self.update_button = tk.Button(self.sub_ads_window,text='Update',command=self._event_update_adsdata)
        self.update_button.pack(padx=5,pady=5,fill="x",side='right')
        self.close_button = tk.Button(self.sub_ads_window,text='Close',command=self.sub_ads_window.destroy)
        self.close_button.pack(padx=5,pady=5,fill="x",side='right')

        with open(self.folderpath+'price.txt',"r+",encoding="utf-8") as tagsf:
            self.price_input.insert(tk.INSERT,tagsf.read())
        with open(self.folderpath+'title.txt',"r+",encoding="utf-8") as tagsf:
            self.title_review.insert(tk.INSERT,tagsf.read())
        with open(self.folderpath+'desc.txt',"r+",encoding="utf-8") as tagsf:
            self.desc_review.insert(tk.INSERT,tagsf.read())
        with open(self.folderpath+'tags.txt',"r+",encoding="utf-8") as tagsf:
            self.tags_review.insert(tk.INSERT,tagsf.read())
        self.sub_ads_window.focus_force()
    
    def __del__(self):
        def filestatus(filename):
            return os.stat(filename).st_size != 0 and os.path.exists(filename)
        
        status = 'OK'
        color='green'
        files=[self.workpath+'title.txt',self.workpath+'price.txt',self.workpath+'desc.txt',self.workpath+'tags.txt',self.workpath+'cate.txt']
        for file in files:
            if not filestatus(file):
                status = 'Not OK'
                color='red'
                break
        self.check_lable.config(text="Current status:"+status,fg=color)
        


    def __checkcategory(self,category):

        cate_path = self.folderpath+'cate.txt'
        current_cate=''
        with open(cate_path,'r',encoding='utf-8') as catef:
            current_cate = catef.read()
        if not len(current_cate)==0:
            if current_cate in category['value']:
                category.set(current_cate)
            else:
                f=open(self.folderpath+'cate.txt', 'w+')
                f.close()
    
    def _event_update_adsdata(self):
        def wedgit_2_txt(wedgit,path):
            if isinstance(wedgit,tk.Text):
                txt = wedgit.get(index1='1.0',index2='end')
                txt = txt.strip()
            else:
                txt = wedgit.get()
            with open(path,'w+',encoding='utf-8') as wtf:
                wtf.write(txt)
        wedgit_2_txt(self.price_input,self.folderpath+'price.txt')
        wedgit_2_txt(self.cate_review,self.folderpath+'cate.txt')
        wedgit_2_txt(self.title_review,self.folderpath+'title.txt')
        wedgit_2_txt(self.desc_review,self.folderpath+'desc.txt')
        wedgit_2_txt(self.tags_review,self.folderpath+'tags.txt')
        messagebox.showinfo("Success","Successfully update!")
        self.sub_ads_window.focus_force()
    
    def _event_import(self,text_wedgit,filename):
        def special_import(text_wedgit=text_wedgit,filename=filename,folderpath=self.folderpath):
            try:
                src_profile_path = filedialog.askopenfilename(filetypes=[("Text files", ".txt")])
                print(src_profile_path)
                if not src_profile_path=="":
                    fc.copy_file(src_profile_path,folderpath+filename)
                with open(folderpath+filename,"r+",encoding="utf-8") as wgtf:
                    text_wedgit.delete('1.0','end')
                    text_wedgit.insert(tk.INSERT,wgtf.read())
                self.sub_ads_window.focus_force()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        return special_import
#-------------------------Class Page------------------------------------


# 创建主窗口
root = tk.Tk()
#root.geometry("400x300")
root.resizable(False,False)
try:
    root.iconbitmap('./Assert/ico/fullsize.ico')
except:
    fc.create_file('./Assert/ico/fullsize.ico')
    root.iconbitmap('./Assert/ico/fullsize.ico')

# 创建GUI对象
my_gui = MyGUI(root)

# 进入主循环
root.mainloop()
