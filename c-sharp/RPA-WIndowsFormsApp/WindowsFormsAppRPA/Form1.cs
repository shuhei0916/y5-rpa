using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Runtime.InteropServices;
using System.Text;
using System.Windows.Forms;

namespace WindowsFormsAppRPA
{
    public partial class Form1 : Form
    {
        [DllImport("user32.dll")]
        static extern bool SetCursorPos(int x, int y);

        public Form1()
        {
            InitializeComponent();
        }

        private void btnClickThis_Click(object sender, EventArgs e)
        {
            lblHelloWorld.Text = "hoge";
            SetCursorPos(100, 100);
        }
    }
}
