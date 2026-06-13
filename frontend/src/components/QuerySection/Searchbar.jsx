import { useEffect, useState } from "react";
import "./Searchbar.css"
import { SearchIcon, ArrowRight } from 'lucide-react'

const Searchbar = () => {

    async function handlesearch(e) {
        e.preventDefault();
    }

    const [query, setquery] = useState("")

    return (
        <form className='search-bar' onSubmit={handlesearch}>
            <SearchIcon className='search-icon' size={22} />
            <input
                type="text"
                placeholder="Describe the movie you are looking for..."
                value={query}
                onChange={(e) => { e.target.value }}
            />
            <button className='search-btn' type='submit'>
                <ArrowRight size={24} />
            </button>
        </form>
    )
}

export default Searchbar