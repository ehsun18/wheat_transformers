"""
Simulation configuration related code goes in here.
- Configuration reader and state object.
- Data structure containing a set of closures for specific functions
  needed by the simulation that we want to make parameters.
- command line argument processing
"""

import os
import configparser
import argparse


class CmdLineArguments:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-c", "--config", help="configuration file.")
        self.args = parser.parse_args()

    def printOut(self):
        print("================")
        print("CmdLineArguments")
        print("================")
        print(str(self.args))
        print("")


class aggregateParameters:
    def __init__(self):
        """
        Create aggregate parameter object with default parameters.
        """
        self.avg_rh_perc = "mean"
        self.avg_temp_c = "mean"
        self.cum_gdd_cday = "mean"
        self.dailyGDD_diff_cday = "mean"
        self.dap = "mean"
        self.diurnal_temp_range_c = "mean"
        self.freezing_dd_cday = "mean"
        self.heat_dd_cday = "mean"
        self.max_rh_perc = "mean"
        self.max_temp_c = "mean"
        self.min_rh_perc = "mean"
        self.min_temp_c = "mean"
        self.potential_evapo_mmday = "mean"
        self.precip_dtr_mmdayc = "mean"
        self.precip_mmday = "sum"
        self.specific_humidity_kgkg = "mean"
        self.sr_wm2 = "mean"
        self.vpd_kpa = "mean"
        self.wet_day_frequency_days = "mean"
        self.wind_speed_ms = "mean"

    def printOut(self):
        print("=================")
        print("aggregateParameters:")
        print("=================")
        print("avg_rh_perc     = " + str(self.avg_rh_perc))
        print("")

    def writeToFile(self, fname):
        config = configparser.RawConfigParser()
        config.add_section("parameters")
        config.set("parameters", "avg_rh_perc", self.avg_rh_perc)
        config.set("parameters", "avg_temp_c", self.avg_temp_c)
        config.set("parameters", "cum_gdd_cday", self.cum_gdd_cday)
        config.set("parameters", "dailyGDD_diff_cday", self.dailyGDD_diff_cday)
        config.set("parameters", "dap", self.dap)
        config.set("parameters", "diurnal_temp_range_c", self.diurnal_temp_range_c)
        config.set("parameters", "freezing_dd_cday", self.freezing_dd_cday)
        config.set("parameters", "heat_dd_cday", self.heat_dd_cday)
        config.set("parameters", "max_rh_perc", self.max_rh_perc)
        config.set("parameters", "max_temp_c", self.max_temp_c)
        config.set("parameters", "min_rh_perc", self.min_rh_perc)
        config.set("parameters", "min_temp_c", self.min_temp_c)
        config.set("parameters", "potential_evapo_mmday", self.potential_evapo_mmday)
        config.set("parameters", "precip_dtr_mmdayc", self.precip_dtr_mmdayc)
        config.set("parameters", "precip_mmday", self.precip_mmday)
        config.set("parameters", "specific_humidity_kgkg", self.specific_humidity_kgkg)
        config.set("parameters", "sr_wm2", self.sr_wm2)
        config.set("parameters", "vpd_kpa", self.vpd_kpa)
        config.set("parameters", "wet_day_frequency_days", self.wet_day_frequency_days)
        config.set("parameters", "wind_speed_ms", self.wind_speed_ms)

        config.add_section("metadata")
        config.set("metadata", "Author", self.Author)
        config.set("metadata", "Notebook", self.Notebook)
        config.set("metadata", "Note", self.cum_gdd_cday)
        config.set("metadata", "Date", self.Date)

        config_dict = {"parameters": parameters, "metadata": metadata}

        os.makedirs(os.path.dirname(fname), exist_ok=True)
        try:
            with open(fname, "w") as configfile:
                config.write(configfile)
        except Exception as e:
            print(f"Error writing to {fname}: {e}")

    def readFromFile(self, fname):
        # X insists to use ConfigParser as opposed to RawConfigParser.
        config = configparser.RawConfigParser()
        config.read(fname)

        self.avg_rh_perc = config.get("parameters", "avg_rh_perc")
        self.avg_temp_c = config.get("parameters", "avg_temp_c")
        self.cum_gdd_cday = config.get("parameters", "cum_gdd_cday")
        self.dailyGDD_diff_cday = config.get("parameters", "dailyGDD_diff_cday")
        self.dap = config.get("parameters", "dap")
        self.diurnal_temp_range_c = config.get("parameters", "diurnal_temp_range_c")
        self.freezing_dd_cday = config.get("parameters", "freezing_dd_cday")
        self.heat_dd_cday = config.get("parameters", "heat_dd_cday")
        self.max_rh_perc = config.get("parameters", "max_rh_perc")
        self.max_temp_c = config.get("parameters", "max_temp_c")
        self.min_rh_perc = config.get("parameters", "min_rh_perc")
        self.min_temp_c = config.get("parameters", "min_temp_c")
        self.potential_evapo_mmday = config.get("parameters", "potential_evapo_mmday")
        self.precip_dtr_mmdayc = config.get("parameters", "precip_dtr_mmdayc")
        self.precip_mmday = config.get("parameters", "precip_mmday")
        self.specific_humidity_kgkg = config.get("parameters", "specific_humidity_kgkg")
        self.sr_wm2 = config.get("parameters", "sr_wm2")
        self.vpd_kpa = config.get("parameters", "vpd_kpa")
        self.wet_day_frequency_days = config.get("parameters", "wet_day_frequency_days")
        self.wind_speed_ms = config.get("parameters", "wind_speed_ms")

        self.Author = config.get("metadata", "Author")
        self.Notebook = config.get("metadata", "Notebook")
        self.Note = config.get("metadata", "Note")
        self.Date = config.get("metadata", "Date")

    def load_config_from_file(self, file_path):
        # Create a ConfigParser object
        config = configparser.ConfigParser()

        # Read the configuration file
        config.read(file_path)

        # Convert the config object to a dictionary of dictionaries
        config_dict = {
            section: dict(config.items(section)) for section in config.sections()
        }

        # Load parameters into the object's attributes
        for name, value in config_dict.get("parameters", {}).items():
            setattr(self, name, value)

    # def readFromFile_v2(self, file_path):
    #     # Create a ConfigParser object
    #     config = configparser.ConfigParser()

    #     # Read the configuration file
    #     config.read(file_path)

    #     # Convert the config object to a dictionary of dictionaries
    #     config_dict = {
    #         section: dict(config.items(section)) for section in config.sections()
    #     }

    #     return config_dict
