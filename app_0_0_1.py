import streamlit as st
from multipage import MultiPage
from spages import SAG25MAY

import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth


# 主页面
###############################################################################
def main_page():
    MAGE_EMOJI_URL = "streamlitbis.png"
    st.set_page_config(page_title='Bisalloy Digital App', page_icon=MAGE_EMOJI_URL, initial_sidebar_state = 'expanded')
    st.markdown(
            f"""
            <style>
                .reportview-container .main .block-container{{
                    max-width: 1800px;
                    padding-top: 0rem;
                    padding-right: 1rem;
                    padding-left: 1rem;
                    padding-bottom: 0rem;
                }}
    
            </style>
            """,
            unsafe_allow_html=True,
        )
    
    
    ####### Actual App Content ########
    app = MultiPage()
    # add applications
    app.add_page('🔵  SAG Mill MAY25', SAG25MAY.app)
    #app.add_page('🟢  SAG Mill #2', SAG25NOV.app)
    app.run()

    # 在侧边栏显示已登录的用户信息
    if 'name' in st.session_state:
        st.sidebar.markdown("User Information")
        st.sidebar.caption(f"username: {st.session_state['name']}")
        st.sidebar.caption(f"account: {st.session_state['username']}")

    if st.sidebar.button("logout"):
        st.session_state['logged_in'] = False
        st.session_state.pop('name', None)
        st.session_state.pop('username', None)
        st.rerun()


# 登录页面
###############################################################################
def login_page():
    MAGE_EMOJI_URL = "streamlitbis.png"
    st.set_page_config(page_title='OptiWear®',page_icon=MAGE_EMOJI_URL, initial_sidebar_state = 'expanded', layout="centered")
    #page_icon = favicon,

    st.markdown(
                f"""
                <style>
                    .reportview-container .main .block-container{{
                        max-width: 1800px;
                        padding-top: 0rem;
                        padding-right: 1rem;
                        padding-left: 1rem;
                        padding-bottom: 0rem;
                    }}
        
                </style>
                """,
                unsafe_allow_html=True,
            )


    st.logo("bisalloy.png")
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )

    name, authentication_status, username = authenticator.login('Bisalloy Digital App', 'main')

    if authentication_status:
        
        st.success(f"Welcome Back!  {name}!")
        st.session_state['logged_in'] = True
        st.session_state['name'] = name  # 存储用户姓名
        st.session_state['username'] = username  # 存储用户名
        st.rerun()  # 刷新页面，跳转到主页面
                    #st.markdown(
                    #    '<nobr><p style="text-align: left;font-family:sans serif; color:#262730; font-size: 23px;">'
                    #    'Welcome to the app gallary. We share the past and most <br> '
                    #    'exciting IoT apps that have been deployed by our team. <br>'
                    #    'Simply click on each app’s URL to view the app.</p></nobr>',
                        #    unsafe_allow_html=True)

    elif authentication_status is False:
        st.error('Username/password is incorrect')
    elif authentication_status is None:
        st.warning('Please enter your username and password')



# 主程序
# Test Auto Deploy
###############################################################################
def main():
    # 初始化登录状态
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    # 根据登录状态显示不同页面
    if st.session_state['logged_in']:
        #app.run()
        main_page()

    else:
        login_page()  # 显示登录页面




# Run application
if __name__ == '__main__':
    main()
