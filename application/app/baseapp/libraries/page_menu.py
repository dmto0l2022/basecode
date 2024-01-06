import dash
from dash import html

def logo_img():
    image_path = dash.get_asset_url('DMToolsLogo.png')
    nav_image = html.Img(src=image_path,style={'height':'33px','padding':'0', 'margin':'0', 'border': '0', 'vertical-align':'middle'})
    return nav_image

def page_top_menu(page_name_in,action_button_in, relevant_dropdowns_in):

    button_padding = {'height':'33px','padding-left':'12px','padding-right':'12px' ,
                          'padding-top':'0px',
                          'padding-bottom':'0px',
                          'margin':'0', 'border': '0', 'vertical-align':'middle'}
    
    baseapp_prefix = '/application/baseapp'
    nav_image = logo_img()
    
    brand_button = html.Button(nav_image, id=page_name_in+"brand_button",
                               className="btn btn-brand",type="button",
                               style=button_padding)
    if action_button_in == '':
        action_button = html.Button("Plot Menu",
                                       id=page_name_in+"plot_menu_button",
                                       className="btn btn-primary",type="button",
                                       style=button_padding)
    else:
        action_button = action_button_in
    
    dropdown_button = html.Button(id=page_name_in + "dropdown_button", type="button",
                               className = "btn btn-danger dropdown-toggle dropdown-toggle-split",
                               **{
                                'data-toggle' : 'dropdown',
                                'aria-haspopup' : 'true',
                                'aria-expanded' : 'false',
                                },
                                children=html.Span(className="sr-only", children=['Main Menu'],
                                                   style={'height':'33px','padding-left':'0px','padding-right':'0px' ,
                                                          'padding-top':'0px',
                                                          'padding-bottom':'0px',
                                                          'margin':'0', 'border': '0', 'vertical-align':'middle'}),
                                  style=button_padding
                              )
    drop_down_separator=  html.A(id=page_name_in + "dropdown_action_plot", children=['--------------'], href=baseapp_prefix + '/', className="dropdown-item")
    drop_down_plot=  html.A(id=page_name_in + "dropdown_action_plot", children=['Plot Menu'], href=baseapp_prefix + '/plot_menu', className="dropdown-item")
    drop_down_data =  html.A(id=page_name_in + "dropdown_action_data", children=['Data Menu'], href=baseapp_prefix + '/data_menu', className="dropdown-item")
    drop_down_admin =  html.A(id=page_name_in + "dropdown_action_admin", children=['Admin Menu'], href=baseapp_prefix + '/admin_menu', className="dropdown-item")
    drop_down_exit =  html.A(id=page_name_in + "dropdown_action_exit", children=['Exit Application'], href=baseapp_prefix + '/', className="dropdown-item")
    drop_down_logout =  html.A(id=page_name_in + "dropdown_action_logout", children=['Logout'], href=baseapp_prefix + '/logout', className="dropdown-item")
    button_list = relevant_dropdowns_in + [drop_down_separator,drop_down_plot,drop_down_data,drop_down_admin, drop_down_exit, drop_down_logout]
    #button_list = [drop_down_plot,drop_down_data,drop_down_admin, drop_down_exit]
  
    dropdown_menu = html.Div(id=page_name_in + "dropdown_menu", children = button_list , className = "dropdown-menu")
    
    split_button = html.Div(children=[brand_button,action_button, dropdown_button, dropdown_menu], className="btn-group",
                            style=button_padding)

    return split_button
