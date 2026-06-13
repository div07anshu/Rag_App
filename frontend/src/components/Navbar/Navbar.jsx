import React from 'react'
import "./Navbar.css"
import { useState } from 'react'
import { Home, Film, History, Info, User } from 'lucide-react'

const Navbar = () => {
    const [active, setActive] = useState("home");
    return (
        <nav>

            <div className='navbar-left'>
                <Film size={36} color="#c084fc" />
                <div>
                    <h3>CineSage</h3>
                    <p>Discover Movies Intelligently</p>
                </div>
            </div>

            <div className='navbar-center'>
                <a href='#'
                    className={active === "home" ? "active" : ""}
                    onClick={() => setActive("home")}>

                    <Home size={20} />
                    Home
                </a>

                <a href='#'
                    className={active === "history" ? "active" : ""}
                    onClick={() => setActive("history")}
                >
                    <History size={20} />
                    History
                </a>

                <a href='#'
                    className={active === "info" ? "active" : ""}
                    onClick={() => setActive("info")}
                >
                    <Info size={20} />
                    About
                </a>
            </div>

            <div className='navbar-right'>
                <button className='profile-btn'>
                    <User color='#c084fc' size={30} />
                </button>
            </div>


        </nav>
    )
}

export default Navbar