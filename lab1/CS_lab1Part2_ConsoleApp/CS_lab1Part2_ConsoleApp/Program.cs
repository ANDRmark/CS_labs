using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CS_lab1Part2_ConsoleApp
{
    class Program
    {
        static void Main(string[] args)
        {
            string pathInput = "input.txt";
            string pathOutput = "output.txt";
            Console.WriteLine("Encode in base64\nInput file name/full path (press enter to use input.txt):");
            string inp = Console.ReadLine();
            if (inp != "")
            {
                pathInput = inp;
                pathOutput = inp + "_b64.txt";
            }
            string pattern = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
            StringBuilder encodingBuilder = new StringBuilder();
            string b64 = "";
            using (FileStream inputFileStream = new FileStream(pathInput,FileMode.Open,FileAccess.Read))
            {
                byte[] buff;
                byte index = 0;
                int amountread = 0;
                do
                {
                    buff = new byte[3];
                    amountread = inputFileStream.Read(buff, 0, buff.Length);
                    if (amountread == 0) break;
                    for (int i = 0; i < buff.Length * 8; i++)
                    {
                        if ((buff[i / 8] & ((byte)1 << 7 - i % 8)) != 0) // on position i is one
                            index = (byte)(index | (byte)1 << (5 - i % 6));
                        if((i+1) % 6 == 0)
                        {
                            if(i - 5  <  amountread * 8)
                                encodingBuilder.Append(pattern[index]);                           
                            else
                                encodingBuilder.Append('=');
                            index = 0;
                        }
                    }

                } while (amountread >= 3);
                inputFileStream.Position = 0;
                buff = new byte[inputFileStream.Length];
                inputFileStream.Read(buff, 0 , buff.Length);
                b64 = Convert.ToBase64String(buff);
            }
            Console.WriteLine("Writing to " + pathOutput);
            StreamWriter output = new StreamWriter(pathOutput, encoding: Encoding.UTF8, append: false);
            if (b64 != encodingBuilder.ToString())
                output.Write("Wrong encoded base 64");
            else
                output.Write(encodingBuilder);
            output.Close();
            Console.WriteLine("Done");
            System.Threading.Thread.Sleep(500);
        }
    }
}
