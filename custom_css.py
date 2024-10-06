from fasthtml.common import *

css = Style('''
    :root {
        --pico-font-size: 100%;
        --pico-font-family: "Arial, sans-serif";
        background-color: #f0f0f0;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    Body {
        min-height: 100vh;
        background: url(/static/background.jpg);
    }
    
    .header-text{
        font-family: 'Times New Roman', Times, serif; 
        color: white;
        font-size: 1.2rem;
    }
    
    .header {   
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        padding: 1.3rem 10%;
        display: flex;
        justify-content:space-between;
        align-items: center;
        z-index: 100;
        background: rgb(0, 0, 0, 0.4);
    }
    
    .header::after{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,.4), transparent);
        transition: .5s;
    }
    
    .header:hover::after{
        left:100%;
    }
    
    .navbar a {
        left: 0;
        position: relative;
        font-size: 1.15rem;
        color: white;
        font.weight: 500;
        text-decoration: none;
        margin-left: 40px;
        opacity: 1;
    }
    
    .navbar a::before {
        content: '';
        top: -4px;
        left: -4px;
        position: absolute;
        width: 110%;
        height: 2px;
        background: white;
        opacity: 0.7;
        z-index: 1;
    }
    
    #check {
        display: none;
    }
    
    .icons{
        position: absolute;
        right: 5%;
        font-size: 2.8rem;
        color: #fff;
        cursor: pointer;
        display: none !important;
    }
    
    /*Breakpoint :v*/
    
    @media (max-width: 767px){
        .icons{
            display: block !important;
        }
        
        #check:checked~.icons #menu-icon {
            display: none;
        }
        
        .icons #close-icon{
            display: none;
        }
        
        #check:checked~.icons #close-icon {
            display: block;
        }
        
        .navbar{
            position: absolute;
            top: 100%;
            left: 0;
            width: 100%;
            height: 0;
            background: rgb(0, 0, 0, 0.2);
            background-filter: blur(50px);
            overflow: hidden;
            transition: .3s ease;
        }
        
        #check:checked~.navbar {
            height: 11.5rem;
        }
        
        .navbar a {
            display: block;
            font-size: 1.1rem;
            margin: 1.5rem;
            text-align: center;
            transform: translateY(-50px);
            opacity: 0;
            transition: .3s ease;
        }
        
        #check:checked~.navbar a {
            transform: translateY(0);
            opacity: 1;
            transition-delay: calc(.15s * var(--i));
        }
        
        .navbar a::before {
            top: -4px;
            text-align: center;
            position: relative;
            height: 2px;
            opacity: 0.7;
            z-index: 1;
            width: 10rem;
        }
    }
    ''')
