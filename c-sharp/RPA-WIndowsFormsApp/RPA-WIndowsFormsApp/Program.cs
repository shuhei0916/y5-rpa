using System;
using System.Collections.Generic;
using System.Windows.Forms;

namespace RPA_WIndowsFormsApp
{
    internal static class Program
    {
        /// <summary>
        /// アプリケーションのメイン エントリ ポイントです。
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new Form1());
            //Console.WriteLine("hello world");
        }
    }
}
