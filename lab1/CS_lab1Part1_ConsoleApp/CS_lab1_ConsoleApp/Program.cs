using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CS_lab1Part1_ConsoleApp
{
    class Program
    {
        static void Main(string[] args)
        {
            //Reading file
            string pathInput = "input.txt";
            string pathOutput = "output.txt";           
            Console.WriteLine("Input file name/full path (press enter to use input.txt)");
            string inp = Console.ReadLine();
            if (inp != "")
            {
                pathInput = inp;
                pathOutput = inp + "_report.txt";
            }

            string allLines;
            using (StreamReader inputFileStream = new StreamReader(pathInput, Encoding.UTF8))
            {
                allLines = inputFileStream.ReadToEnd();
            }
            Console.WriteLine(allLines);

            //Processing file
            Console.WriteLine("Writing to " + pathOutput);
            StreamWriter output = new StreamWriter(pathOutput, encoding: Encoding.UTF8, append: false);
            Dictionary<char, int> charcounts = new Dictionary<char, int>();
            int charNum = 0;
            foreach(char ch in allLines)
            {
                //if(Char.IsLetter(ch))
                {
                    if (charcounts.ContainsKey(/*Char.ToLower*/(ch)))
                        charcounts[/*Char.ToLower*/(ch)]++;
                    else
                        charcounts[/*Char.ToLower*/(ch)] = 1;
                    charNum++;
                }
            }
            output.WriteLine("Number of chars: "+charNum);
            output.WriteLine("Char counts: ");
            foreach (var kvp in charcounts.OrderBy((a) => a.Key))
            {
                output.WriteLine(kvp.Key + " --> " + kvp.Value);
            }

            //calculate char frequencies
            Dictionary<char, double> charFrequencies = new Dictionary<char, double>();
            foreach (var kvp in charcounts.OrderBy((a) => a.Key))
            {
                charFrequencies[kvp.Key] = (double)kvp.Value / (double)charNum;
            }
            output.WriteLine();
            output.WriteLine("Char frequencies: ");
            foreach (var kvp in charFrequencies.OrderBy((a) => a.Key))
            {
                output.WriteLine(kvp.Key + " --> " + kvp.Value);
            }
            // Average entropy    
            output.WriteLine();
            double avgEntropy = 0;
            foreach(var kvp in charFrequencies)
            {
                avgEntropy += kvp.Value * Math.Log(1 / kvp.Value, 2);
            }
            output.WriteLine("Average entropy: " + avgEntropy);

            // amount of information
            output.WriteLine();
            output.WriteLine("Amount of information: " + (avgEntropy * charNum));
            output.WriteLine("Amount of information (divided by 8): " + (avgEntropy * charNum) / 8.0);
            output.WriteLine("File size in bytes: "+ new System.IO.FileInfo(pathInput).Length);

            //
            output.Close();
            Console.WriteLine("Done");
            System.Threading.Thread.Sleep(500);
        }
    }
}
