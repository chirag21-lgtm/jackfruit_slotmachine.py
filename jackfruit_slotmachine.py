import wx, random, time

SYMBOLS = ["🍒","🍋","🔔","⭐"]

class Slot(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Slot Machine", size=(400,420))
        p = wx.Panel(self)
        p.SetBackgroundColour("#222831")

        self.balance = 0

        # Title
        title = wx.StaticText(p, label="🎰 Slot Machine")
        title.SetFont(wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        title.SetForegroundColour("#FFD369")

        # Reels
        self.reels = [wx.StaticText(p, label="❔") for _ in range(3)]
        for r in self.reels:
            r.SetFont(wx.Font(36, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            r.SetForegroundColour("white")

        # Deposit + Bet
        self.dep = wx.TextCtrl(p, value="100", size=(70,-1))
        self.bet = wx.TextCtrl(p, value="10", size=(70,-1))

        dep_btn = wx.Button(p, label="Deposit")
        dep_btn.Bind(wx.EVT_BUTTON, self.deposit)

        spin_btn = wx.Button(p, label="SPIN", size=(200,55))
        spin_btn.SetBackgroundColour("#FFD369")
        spin_btn.Bind(wx.EVT_BUTTON, self.spin)

        self.msg = wx.StaticText(p, label="", style=wx.ALIGN_CENTER)
        self.msg.SetForegroundColour("white")

        self.bal = wx.StaticText(p, label="Balance: 0")
        self.bal.SetForegroundColour("white")

        # Layout
        v = wx.BoxSizer(wx.VERTICAL) 
        v.Add(title, 0, wx.ALIGN_CENTER|wx.TOP, 10)

        h = wx.BoxSizer(wx.HORIZONTAL)
        for r in self.reels: h.Add(r,1,wx.ALIGN_CENTER|wx.ALL,10)
        v.Add(h,1,wx.ALIGN_CENTER)

        row1 = wx.BoxSizer(wx.HORIZONTAL)
        row1.Add(wx.StaticText(p,label="Deposit:"),0,wx.RIGHT,5)
        row1.Add(self.dep,0,wx.RIGHT,10)
        row1.Add(dep_btn,0)
        v.Add(row1,0,wx.ALIGN_CENTER|wx.TOP,10)

        row2 = wx.BoxSizer(wx.HORIZONTAL)
        row2.Add(wx.StaticText(p,label="Bet:"),0,wx.RIGHT,5)
        row2.Add(self.bet,0)
        v.Add(row2,0,wx.ALIGN_CENTER|wx.TOP,10)

        v.Add(spin_btn,0,wx.ALIGN_CENTER|wx.TOP,15)
        v.Add(self.msg,0,wx.ALIGN_CENTER|wx.TOP,10)
        v.Add(self.bal,0,wx.ALIGN_CENTER|wx.TOP,5)

        p.SetSizer(v)
        self.Centre(); self.Show()

    def deposit(self, e):
        try:
            amt = int(self.dep.GetValue())
            if amt > 0:
                self.balance += amt
                self.bal.SetLabel(f"Balance: {self.balance}")
                self.msg.SetLabel(f"✅ Deposited {amt}")
        except:
            self.msg.SetLabel("❌ Invalid deposit")

    def spin(self, e):
        try:
            bet = int(self.bet.GetValue())
            if bet <= 0 or bet > self.balance:
                self.msg.SetLabel("❌ Invalid bet")
                return
        except:
            self.msg.SetLabel("❌ Invalid bet")
            return

        self.balance -= bet

        # Spin animation
        for _ in range(10):
            for r in self.reels:
                r.SetLabel(random.choice(SYMBOLS))
            wx.Yield(); time.sleep(0.05)

        r1, r2, r3 = [r.GetLabel() for r in self.reels]

        if r1 == r2 == r3:
            win = bet * 10
            self.balance += win
            self.msg.SetLabel(f"🎉 JACKPOT! Won {win}")
        else:
            self.msg.SetLabel("❌ You Lost")

        self.bal.SetLabel(f"Balance: {self.balance}")

if __name__ == "__main__":
    app = wx.App()
    Slot()
    app.MainLoop()