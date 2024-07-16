using System;
using System.Collections.Generic;
using System.Text;
//using System.Windows.Forms;
//using System.Drawing;

namespace RPA_ConsoleApp
{
    internal class Program
    {
        [System.Runtime.InteropServices.DllImport("user32.dll")]
        static extern bool SetCursorPos(int x, int y);

        static void Main(string[] args)
        {
            Console.WriteLine("hoge");

            //// マウスの現在の座標を取得
            //Point currentPosition = Cursor.Position;
            //Console.WriteLine($"現在のマウス座標: X={currentPosition.X}, Y={currentPosition.Y}");

        }
    }
}
