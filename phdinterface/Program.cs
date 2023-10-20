using CommandLine;
using ConsoleApp8;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Security;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Input;
using Uniformance.PHD;

namespace ConsoleApp8
{
    
    [Verb("getdata", HelpText = "Returns data from a tag as XML.")]
    class dataOptions
    {
        //[Option('h', "hostname", Required = true, HelpText = "Servname")]
        [Option('h', "hostname", Default = "MALSHW1", HelpText = "Servname")]
        public string Hostname { get; set; }

        [Option('u', "username", Default = "", HelpText = "Username")]
        public string UserName { get; set; }

        [Option('p', "password", Default = "", HelpText = "Password")]
        public string Password { get; set; }

        [Option('P', "port", Default = 3000, HelpText = "Port")]
        public int Port { get; set; }

        // Default = "A.RL_AI7361.BATCH"
        [Option('t', "tag", HelpText = "Tag")]
        public string Tag { get; set; }

        [Option('s', "starttime", Default = "NOW-1D", HelpText = "StartTime")]
        public string StartTime { get; set; }

        [Option('e', "endtime", Default = "NOW", HelpText = "EndTime")]
        public string EndTime { get; set; }

        [Option('f', "samplefrequency", HelpText = "Sample Frequency")]
        public uint Frequency { get; set; }

        [Option('g', "usesamplefrequency", Default =false, HelpText = "Enable Sample Frequency")]
        public Boolean UseSampleFrequency { get; set; }

        [Option('F', "samplefrequencytype", Default =SAMPLETYPE.Raw ,HelpText = "Sample Type: Snapshot, Average, Raw")]
        public  SAMPLETYPE SampleFrequencyType { get; set; }

        [Option('R', "reductiontype", HelpText = "Sample Type: Snapshot, Average, Raw")]
        public REDUCTIONTYPE ReductionType { get; set; } 

        [Option('r', "reductionfrequency", HelpText = "Sample Type: Snapshot, Average, Raw")]
        public uint ReductionFrequency { get; set; }

        [Option('o', "ReductionOffset", HelpText = "The ReductionOffset property identifies the offset applied when retrieving reductions: After, Around, Before")]
        public REDUCTIONOFFSET ReductionOffset { get; set; }

    }

    [Verb("checktag", HelpText = "Record changes to the repository.")]
    class checkOptions
    {
        [Option('h', "hostname", Default = "MALSHW1", HelpText = "Servname")]
        public string Hostname { get; set; }

        [Option('u', "username", Default = "", HelpText = "Username")]
        public string UserName { get; set; }

        [Option('p', "password", Default = "", HelpText = "Password")]
        public string Password { get; set; }

        [Option('P', "port", Default = 3000, HelpText = "Port")]
        public int Port { get; set; }

        [Option('t', "tag", Default = "", HelpText = "Tag")]
        public string Tag { get; set; }
    }



    internal class Program
    {
        static int Main(string[] args)
        {
            return CommandLine.Parser.Default.ParseArguments<dataOptions, checkOptions>(args).MapResult(
                (dataOptions opts) => RundataOptions(opts),
                (checkOptions opts) => RuncheckOptions(opts),
      
                errs => 1);
        }

        static int RundataOptions(dataOptions opts)
        {
            var u = new PHDServer();
            var h = new PHDHistorian();
            var tags = new Tags();

            u.HostName = opts.Hostname;
            u.UserName = opts.UserName;
            u.Password = opts.Password;

            h.StartTime = opts.StartTime;
            h.EndTime = opts.EndTime;
            h.UseSampleFrequency = opts.UseSampleFrequency;
            h.SampleFrequency = opts.Frequency;
            h.Sampletype = opts.SampleFrequencyType;
            h.ReductionFrequency = opts.ReductionFrequency;
            h.ReductionType = opts.ReductionType;
            h.ReductionOffset = opts.ReductionOffset;




            if (opts.Port != 3000) { u.Port = opts.Port; }
            h.DefaultServer = u;
            if (opts.Tag != null) {
                var phdtag = new Tag(opts.Tag);
                tags.Add(phdtag);
                var data = h.FetchRowData(tags);
                Console.WriteLine(data.GetXml());
            }
            return 0;
            
        }

        static int RuncheckOptions(checkOptions opts)
        {
            var u = new PHDServer();
            var h = new PHDHistorian();
            var tags = new Tags();

            u.HostName = opts.Hostname;
            u.UserName = opts.UserName;
            u.Password = opts.Password;
            if (opts.Port != 3000) { u.Port = opts.Port; }
            h.DefaultServer = u;

            try
            {
                if (h.GetPHDTagname(opts.Tag) == "")
                {
                    Console.WriteLine($"{opts.Tag} does not exist in system");
                    return 1;
                }
                else
                {
                    Console.WriteLine($"{opts.Tag} found");
                }
            }
            catch (ArgumentException e)
            {
                Console.WriteLine($"Server Connection Failed Check Details: {e.Message}");
                return 1;
            }

            return 0;

        }
        static void HandleParseError(IEnumerable<Error> errs)
        {
            //handle errors
        }
    }
}