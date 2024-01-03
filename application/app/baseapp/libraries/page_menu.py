import dash
from dash import html

def logo_img():
    image_path = dash.get_asset_url('DMToolsLogo.png')
    nav_image = html.Img(src=image_path,style={'height':'33px','padding':'0', 'margin':'0'})
    return nav_image

def page_top_menu(page_name_in, relevant_dropdowns_in, logo_img_in):

    baseapp_prefix = '/application/baseapp'
    nav_image = logo_img_in
    
    brand_button = html.Button(nav_image, id=page_name_in+"brand_button", className="btn btn-brand",type="button")
    
    plot_menu_button = html.Button("Plot Menu", id=page_name_in+"plot_menu_button", className="btn btn-primary",type="button")
    
    dropdown_button = html.Button(id=page_name_in + "dropdown_button", type="button",
                               className = "btn btn-danger dropdown-toggle dropdown-toggle-split",
                               **{
                                'data-toggle' : 'dropdown',
                                'aria-haspopup' : 'true',
                                'aria-expanded' : 'false',
                                },
                                children=html.Span(className="sr-only", children=['Main Menu'])
                              )
    
    drop_down_plot=  html.A(id=page_name_in + "dropdown_action_plot", children=['Plot'], href=baseapp_prefix + '/plot_menu', className="dropdown-item")
    drop_down_data =  html.A(id=page_name_in + "dropdown_action_data", children=['Data'], href=baseapp_prefix + '/data_menu', className="dropdown-item")
    drop_down_admin =  html.A(id=page_name_in + "dropdown_action_admin", children=['Admin'], href=baseapp_prefix + '/admin_menu', className="dropdown-item")
    drop_down_exit =  html.A(id=page_name_in + "dropdown_action_exit", children=['Exit'], href=baseapp_prefix + '/', className="dropdown-item")
    #button_list = relevant_dropdowns_in + [drop_down_plot,drop_down_data,drop_down_admin, drop_down_exit]
    button_list = [drop_down_plot,drop_down_data,drop_down_admin, drop_down_exit]
  
    dropdown_menu = html.Div(id=page_name_in + "dropdown_menu", children = button_list , className = "dropdown-menu")
    
    split_button = html.Div(children=[brand_button,plot_menu_button, dropdown_button, dropdown_menu], className="btn-group",
                            style={'top': '0px','left': '0','right':'0','height':'33px'})

    return split_button
