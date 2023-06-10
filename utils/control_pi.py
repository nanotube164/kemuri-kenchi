import sys
import clr

sys.path.append(r'C:\Program Files (x86)\PIPC\AF\PublicAssemblies\4.0')
clr.AddReference('OSIsoft.AFSDK')
from OSIsoft.AF.PI import *
from OSIsoft.AF.UnitsOfMeasure import *
import datetime
import pandas as pd
import numpy as np
from pandas import *
from OSIsoft.AF import *
from OSIsoft.AF.Search import *
from OSIsoft.AF.Asset import *
from OSIsoft.AF.Data import *
from OSIsoft.AF.Time import *

class OSIsoftPy(object):

    # CONNECT TO PI SERVER
    def connect_to_Server(serverName):
        piServers = PIServers()
        global piServer
        piServer = piServers[serverName]  # Write PI Server Name
        piServer.Connect(False)  # Connect to PI Server
        print('Connected to server: ' + serverName)

    # CONNECT TO AF SERVER AND PRINT ATTRIBUTE VALUE
    def connect_to_AF(AFserverName, Database, Tech, Plant, Unit, Attribute):
        afServers = PISystems()
        afServer = afServers[AFserverName]  # Write AF Server Name
        afServer.Connect()  # Connect to AF Server
        DB = afServer.Databases.get_Item(Database)  # Define architecture
        element = DB.Elements.get_Item(Tech).Elements.get_Item(
            Plant).Elements.get_Item(Plant + " " + Unit)
        attribute = element.Attributes.get_Item(Attribute)
        attval = attribute.GetValue()
        # Print Attributr Value
        print('Element Name: {0}'.format(element.Name))
        print('Attribute Name: {0} \nValue: {1} \nUOM: {2}'.format(
            attribute.Name, attval.Value, attribute.DefaultUOM))

    # WRITE TAG VALUE IN PI TAG
    def write_tag(tagname, value, datetime):
        # Select PI Server and Tag name
        writept = PIPoint.FindPIPoint(piServer, tagname)
        val = AFValue(value, AFTime(datetime))  # Select Value and Timestamp
        writept.UpdateValue(val, AFUpdateOption.Replace,
                            AFBufferOption.BufferIfPossible)  # Write value
        print('Tag "' + tagname + '" updated.')  # Print Tag Name updated
    
    # WRITE TAG VALUE IN PI TAG (不壓縮資料)
    def write_tag2(tagname, value, datetime):
        # Select PI Server and Tag name
        writept = PIPoint.FindPIPoint(piServer, tagname)
        val = AFValue(value, AFTime(datetime))  # Select Value and Timestamp
        writept.UpdateValue(val, AFUpdateOption.InsertNoCompression,
                            AFBufferOption.BufferIfPossible)  # Write value
        print('Tag "' + tagname + '" updated.')  # Print Tag Name updated
        
    # WRITE TAG VALUE IN PI TAG (不壓縮資料)
    def write_tag3(tagname, value, datetime):
        # Select PI Server and Tag name
        writept = PIPoint.FindPIPoint(piServer, tagname)
        val = AFValue(value, AFTime(datetime))  # Select Value and Timestamp
        writept.UpdateValue(val, AFUpdateOption.Remove,
                            AFBufferOption.BufferIfPossible)  # Write value
        print('Tag "' + tagname + '" updated.')  # Print Tag Name updated

    # GET SNAPSHOT TAG VALUE
    def get_tag_snapshot(tagname):
        tag = PIPoint.FindPIPoint(piServer, tagname)
        lastData = tag.Snapshot()  # Get Snapshot
        # print ('Last Value in PI Tag ' + tagname + ' = ' + str(lastData))                   #Print Tag Value
        return lastData.Value, lastData.Timestamp.ToString("yyyy-MM-dd HH:mm:ss")

    # GET SAMPLED VALUES
    def sampled_values(tagname, initdate, enddate, span):
        # Select PI Server and Tag name
        tag = PIPoint.FindPIPoint(piServer, tagname)
        # Select Time Range (Osisoft PI format)
        timerange = AFTimeRange(initdate, enddate)
        sampled = tag.InterpolatedValues(timerange, AFTimeSpan.Parse(
            span), '', False)  # Get Sampled Values (IMPORTANT: Define Span)
        # print('\nShowing sampled values in PI Tag {0}'.format(tagname))                     #Print Sampled Values
        # for event in sampled:
        #     print('{0} value: {1}'.format(event.Timestamp.LocalTime, event.Value))
        return sampled

        # GET SAMPLED VALUES 改版
    def sampled_values_dict(tagname, initdate, enddate, span):
        # Select PI Server and Tag name
        tag = PIPoint.FindPIPoint(piServer, tagname)
        # Select Time Range (Osisoft PI format)
        timerange = AFTimeRange(initdate, enddate)
        sampled = tag.InterpolatedValues(timerange, AFTimeSpan.Parse(
            span), '', False)  # Get Sampled Values (IMPORTANT: Define Span)
        print('\nShowing sampled values in PI Tag {0}'.format(
            tagname))  # Print Sampled Values
        sampled_dict = {}
        for event in sampled:
            temp_datetime = event.Timestamp.LocalTime.ToString().replace(
                "上午", "AM").replace("下午", "PM")
            temp_datetime = datetime.datetime.strptime(
                temp_datetime, '%Y/%m/%d %p %I:%M:%S')
            #temp_datetime = datetime.strptime(temp_datetime, '%m/%d/%Y %H:%M:%S %p')
            temp_datetime = temp_datetime.strftime("%Y/%m/%d")
            sampled_dict.update({temp_datetime: event.Value})
            print('{0} value: {1}'.format(
                event.Timestamp.LocalTime, event.Value))
        return sampled_dict

    # GET RECORDED VALUES
    def recorded_values(tagname, initdate, enddate):
        # Select PI Server and Tag name
        tag = PIPoint.FindPIPoint(piServer, tagname)
        # Select Time Range (Osisoft PI format)
        timerange = AFTimeRange(initdate, enddate)
        # Get Recorded Values in Time Range
        recorded = tag.RecordedValues(
            timerange, AFBoundaryType.Inside, "", False)
        print('\nShowing recorded values in PI Tag {0}'.format(tagname))                    #Print Recorded Values
        for event in recorded:
            print('{0} value: {1}'.format(event.Timestamp.LocalTime, event.Value))
        return recorded
    
    # GET RECORDED VALUES 改版
    def recorded_values_dict(tagname, initdate, enddate):
        # Select PI Server and Tag name
        tag = PIPoint.FindPIPoint(piServer, tagname)
        # Select Time Range (Osisoft PI format)
        timerange = AFTimeRange(initdate, enddate)
        # Get Recorded Values in Time Range
        recorded = tag.RecordedValues(
            timerange, AFBoundaryType.Inside, "", False)
        record_dict = {}
        for event in recorded:
            temp_datetime = event.Timestamp.LocalTime.ToString().replace("上午", "AM").replace("下午", "PM")
            temp_datetime = datetime.datetime.strptime(temp_datetime, '%Y/%m/%d %p %I:%M:%S')
            temp_datetime = temp_datetime.strftime("%Y/%m/%d %H:%M:%S'")
            record_dict.update({temp_datetime: event.Value})
            print('{0} value: {1}'.format(
                event.Timestamp.LocalTime, event.Value))
        return record_dict

    # FIND TAGS
    def find_tags(mask):
        # Select PI Server and Mask
        points = PIPoint.FindPIPoints(piServer, mask, None, None)
        points = list(points)
        return [print(i.get_Name()) for i in points]  # Print coincidences

    # DELETE TAG VALUES IN PI TAG
    def delete_values(tagname, initdate, enddate):
        # Select PI Server and Tag Name
        deleteval = PIPoint.FindPIPoint(piServer, tagname)
        # Select Time Range (Osisoft PI format)
        timerange = AFTimeRange(initdate, enddate)
        # Get Recorded Values in Time Range
        recorded = deleteval.RecordedValues(
            timerange, AFBoundaryType.Inside, "", False)
        # Delete Recorded Values in Time Range
        deleteval.UpdateValues(recorded, AFUpdateOption.Remove)
        print('\nTag Values selected of PI Tag "' + tagname +
              '" have been deleted.')  # Print Tag Name updated

    # UPDATE AF ATTRIBUTES
    def update_AF_attribute(AFserverName, Database, Elem, Tech, Plant, Unit, Attribute1, Value1, Attribute2, Value2):
        afServers = PISystems()
        afServer = afServers[AFserverName]
        DB = afServer.Databases.get_Item(Database)
        element = DB.Elements.get_Item(Elem).Elements.get_Item(
            Tech).Elements.get_Item(Plant).Elements.get_Item(Unit)
        attribute = element.Attributes.get_Item(Attribute1)
        attribute.SetValue(AFValue(Value1))
        attribute = element.Attributes.get_Item(Attribute2)
        attribute.SetValue(AFValue(Value2))

    # def Average_Value(tagname, initdate, enddate, span):
#     def Average_Value(tagname, initdate, enddate, span):
#         tag = PIPoint.FindPIPoint(piServer, tagname)
#         timerange = AFTimeRange(initdate, enddate)
# #         summaries = tag.Summaries(timerange,AFTimeSpan.Parse(span), AFSummaryTypes.Average, AFCalculationBasis.TimeWeighted, AFTimestampCalculation.Auto)
#         summaries = tag.Summaries(timerange, AFTimeSpan.Parse(span), 2, 0, 2)
#         L = []
#         for summary in summaries:
#             for event in summary.Value:
#                 f = event.Timestamp.LocalTime
#                 v = event.Value
#                 L.append([f, v])
#             df = pd.DataFrame(L, columns=['Timestamp', tagname])
#             return df
    def Average_Value(tagname, initdate, enddate, span):
        tag = PIPoint.FindPIPoint(piServer, tagname)
        timerange = AFTimeRange(initdate, enddate)
#         summaries = tag.Summaries(timerange,AFTimeSpan.Parse(span), AFSummaryTypes.Average, AFCalculationBasis.TimeWeighted, AFTimestampCalculation.Auto)
        summaries = tag.Summaries(timerange, AFTimeSpan.Parse(span), 2, 0, 2)
        L = []
        for summary in summaries:
            for event in summary.Value:
                f = event.Timestamp.ToString("yyyy-MM-dd HH:mm:ss")
                t = tagname
                v = event.Value
                L.append([f, t, v])
            df = pd.DataFrame(L, columns=['Timestamp', 'Tag', 'Value'])
            return df

    def get_pi_sampled_values(tagname, initdate, enddate):
        # Select PI Server and Tag name
        tag = PIPoint.FindPIPoint(piServer, tagname)
        # Select Time Range (Osisoft PI format)
        timerange = AFTimeRange(initdate, enddate)
        sampled = tag.RecordedValues(
            timerange, AFBoundaryType.Inside, "", False)
        L = []
        for event in sampled:
            f = event.Timestamp.ToString("yyyy-MM-dd HH:mm:ss")
            t = tagname
            v = event.Value
            L.append([f, t, v])
            df = pd.DataFrame(L, columns=['Timestamp', 'Tag', 'Value'])
            return df
