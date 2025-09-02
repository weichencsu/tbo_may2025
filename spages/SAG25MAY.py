# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from io import BytesIO

def process_sensor_data(file_path):
 
    # 读取Excel文件中的所有Sheet
    xls = pd.ExcelFile(file_path)
    sheets_dict = pd.read_excel(xls, sheet_name=None)
    
    # 初始化结果列表
    results = []
    
    # 遍历每个Sheet进行处理
    for sheet_name, df in sheets_dict.items():
        # 检查是否存在需要过滤的列
        if '总长_DEC' in df.columns:
            # 过滤掉总长_DEC等于12337的行
            filtered_df = df[df['总长_DEC'] != 12337]
        else:
            # 如果列不存在，保留原数据（或根据需求处理）
            filtered_df = df
        
        # 检查过滤后的DataFrame是否为空
        if filtered_df.empty:
            # 记录空数据的情况
            results.append({
                'sensorName': sheet_name,
                'latestTime': None,
                'totalLength': None,
                'actualLength': None
            })
        else:
            # 获取最后一行数据
            last_row = filtered_df.iloc[-1]
            # 提取所需字段，使用.get()避免KeyError
            latest_time = last_row.get('time')
            total_length = last_row.get('总长_DEC')
            actual_length = last_row.get('实际长度_DEC')
            
            results.append({
                'sensorName': sheet_name,
                'latestTime': latest_time,
                'totalLength': total_length,
                'actualLength': actual_length
            })
    
    # 转换结果列表为DataFrame
    result_df = pd.DataFrame(results)
    
    return result_df


def plot_sensor_data(file_path):
    # 读取所有sheet
    sheets = pd.read_excel(file_path, sheet_name=None)
    
    # 创建图形对象
    fig = go.Figure()
    
    # 处理每个sheet
    for sheet_name, df in sheets.items():
        # 过滤数据
        filtered_df = df[df['总长_DEC'] != 12337]
        
        # 转换时间格式
        filtered_df['time'] = pd.to_datetime(filtered_df['time'])
        
        # 添加轨迹到图形
        fig.add_trace(go.Scatter(
            x=filtered_df['time'],
            y=filtered_df['实际长度_DEC'],
            mode='lines+markers',
            name=sheet_name
        ))
    # Add horizontal lines
    fig.add_hline(y=150, line_dash="dash", line_width=2, line_color="orange", annotation_text="Lifter Reline Limit 150mm")
    fig.add_hline(y=120, line_dash="solid", line_width=3, line_color="red", annotation_text="Lifter Failure Limit 120mm")
    fig.add_hline(y=40, line_dash="dash", line_width=2, line_color="orange", annotation_text="Plate Reline Limit 40mm")
    fig.add_hline(y=30, line_dash="solid", line_width=3, line_color="red", annotation_text="Plate Failure Limit 30mm")
        
    # Update axis format
    fig.update_yaxes(title_text="Sensor Length - mm")
    fig.update_xaxes(title_text="Date and Time")
    fig.update_yaxes(range=[0, 450])

    # Update figure format
    fig.update_layout(
        margin=dict(l=1, r=1, t=30, b=1),
        template="seaborn"
    )
    
    # 设置布局
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.9,
            xanchor="right",
            x=1
        )
    )
    
    return fig


def downloadData(file_path):
    # 定义新的列名
    NEW_COLUMNS = [
        "Datetime", 
        "TotalLength(HEX)", 
        "SensorID(HEX)", 
        "CurrentLength(HEX)", 
        "CheckCode(HEX)", 
        "TotalLength(mm)", 
        "SensorID", 
        "CurrentLength(mm)", 
        "CheckCode"
    ]

    try:
        # 读取所有工作表（返回字典格式：{sheet_name: DataFrame}）
        with pd.ExcelFile(file_path) as excel_file:
            # 创建内存缓冲区
            output = BytesIO()
            
            # 使用ExcelWriter将处理后的数据写入内存
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                # 遍历每个工作表
                for sheet_name in excel_file.sheet_names:
                    df = pd.read_excel(excel_file, sheet_name=sheet_name)
                    
                    # 检查列数是否匹配
                    if len(df.columns) != len(NEW_COLUMNS):
                        raise ValueError(f"工作表 '{sheet_name}' 列数不匹配："
                                        f"需要 {len(NEW_COLUMNS)} 列，实际 {len(df.columns)} 列")
                    
                    # 重命名列
                    df.columns = NEW_COLUMNS
                    
                    # 写入新的Excel文件
                    df.to_excel(
                        writer,
                        sheet_name=sheet_name,
                        index=False
                    )
            
            # 创建下载按钮
            st.download_button(
                label=":material/Download:  Download Database",
                data=output.getvalue(),
                file_name=file_path,
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                use_container_width = True
            )
            
            st.success("Sensor database available. Please click button to download!!!")    

    except FileNotFoundError:
        st.error(f"文件未找到：{file_path}")
        st.info("请确认文件路径和权限")
    except Exception as e:
        st.error(f"发生错误：{str(e)}")









def app():
    ######################## User Input #######################
    ### 分别读取设备名称的传感器数据库结果，并传递至Streamlit 前端进行显示
    ### FE, MID, DE被分为三个表，分别导入
    FE_databasedPath = 'FE2025May_Database_update.xlsx'      # FE
    FE_sensorResults = process_sensor_data(FE_databasedPath)

    MID_databasedPath = 'MID2025May_Database_update.xlsx'      # MID
    MID_sensorResults = process_sensor_data(MID_databasedPath)

    DE_databasedPath = 'DE2025May_Database_update.xlsx'      # DE
    DE_sensorResults = process_sensor_data(DE_databasedPath)

    ##  "sensorName  latestTime  totalLength  actualLength" ###
    ######################## End of User Input ################






    ###################      Start of App     ###############################
    st.subheader("SAG Mill May2025 Wear Sensor Installation", divider = 'rainbow')
    # st.subheader("", divider='red')


    ############################## Section 1 ################################

    st.markdown("1. Wear Sensor Installation Details")

    FE_drawing, MID_drawing, DE_drawing = st.tabs(["FE Shell", "MID Shell", "DE Shell"])
    with FE_drawing:
        st.image("FE.png", caption = "Sensor Install Locations", use_container_width = True)
    with MID_drawing:
        st.image("MID.png", caption = "Sensor Install Locations", use_container_width = True)
    with DE_drawing:
        st.image("DE.png", caption = "Sensor Install Locations", use_container_width = True)
        
    st.markdown("###")

    ############################## Section 2 ################################n   
    st.markdown("2. Wear Sensor Live Status")

    FE_sensor, MID_sensor, DE_sensor = st.tabs(["FE Shell Sensors", "MID Shell Sensors", "DE Shell Sensors"])
    with FE_sensor:
        for row in FE_sensorResults.itertuples():
            # 检查 totalLength 是否非空（非 NaN）
            if pd.notna(row.totalLength):
                st.caption("Latest Reading at: " + str(row.latestTime))
                st.metric(label = ":material/Sensors: " +  row.sensorName + " Sensor Reading", value = str(row.actualLength) + "mm", delta = row.actualLength - row.totalLength, border=True)
            else:
                st.metric(label = ":material/Sensors: " +  row.sensorName + " Sensor Reading", value = "No Wear Data Received", border=True)
            #st.markdown("###")
        # 绘制时间序列图
        st.markdown("Wear Sensor Plots")
        
        # Specify the file path
        fig1 = plot_sensor_data(FE_databasedPath)
        st.plotly_chart(fig1, use_container_width=True)

        # data download function
        downloadData(FE_databasedPath)


    with MID_sensor:
        for row in MID_sensorResults.itertuples():
            # 检查 totalLength 是否非空（非 NaN）
            if pd.notna(row.totalLength):
                st.caption("Latest Reading at: " + str(row.latestTime))
                st.metric(label = ":material/Sensors: " +  row.sensorName + " Sensor Reading", value = str(row.actualLength) + "mm", delta = row.actualLength - row.totalLength, border=True)
            else:
                st.metric(label = ":material/Sensors: " +  row.sensorName + " Sensor Reading", value = "No Wear Data Received", border=True)    
            #st.markdown("###")
        # 绘制时间序列图
        st.markdown("Wear Sensor Plots")
        
        # Specify the file path
        fig2 = plot_sensor_data(MID_databasedPath)
        st.plotly_chart(fig2, use_container_width=True)
    
        # data download function
        downloadData(MID_databasedPath)

    with DE_sensor:
        for row in DE_sensorResults.itertuples():
            # 检查 totalLength 是否非空（非 NaN）
            if pd.notna(row.totalLength):
                st.caption("Latest Reading at: " + str(row.latestTime))
                st.metric(label = ":material/Sensors: " +  row.sensorName + " Sensor Reading", value = str(row.actualLength) + "mm", delta = row.actualLength - row.totalLength, border=True)
            else:
                st.metric(label = ":material/Sensors: " +  row.sensorName + " Sensor Reading", value = "No Wear Data Received", border=True)    
            #st.markdown("###")
        # 绘制时间序列图
        st.markdown("Wear Sensor Plots")
        
        # Specify the file path
        fig3 = plot_sensor_data(DE_databasedPath)
        st.plotly_chart(fig3, use_container_width=True)
        
        # data download function
        downloadData(DE_databasedPath)

    st.markdown("###")
################################## plot data ###############################################
    ################################## 3D Model ###############################################
    #st.markdown("###")
    #st.markdown("4. 3D Liner Model")
    #iframeLINK = "https://kitware.github.io/glance/app/?name=millShellWearMonitoring.vtkjs&url=https://webify-1306024390.cos.ap-shanghai.myqcloud.com/millShellWearMonitoring.vtkjs"
    #local_pvModel(iframeLINK)
    #pvOBJ = read_file_from_url(iframeLINK)
    #components.html(pvOBJ, height=1000)
    
    #HtmlFile_tSS1 = open("hydrocyclone.html", 'r', encoding='utf-8').read()
    #components.html(HtmlFile_tSS1, height=1000)

    #st.write(
    #        f'<iframe src=' + iframeLINK + ' height = "800" width = "100%"></iframe>',
    #        unsafe_allow_html=True,
    #)
    ############################## Section Display Dataframe ################################
    st.markdown("###")





