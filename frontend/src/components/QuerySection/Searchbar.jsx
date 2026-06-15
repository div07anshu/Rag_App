import { useState } from "react";
import "./Searchbar.css"
import { SearchIcon, ArrowRight } from 'lucide-react'

const Searchbar = ({ setmovies, setloading }) => {

    async function handlesearch(e) {
        e.preventDefault();
        setloading(true);

        try {
            const response = await fetch(
                "ragapp-production-b45d.up.railway.app", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    ques: query,
                })
            })

            const data = await response.json()
            setmovies(data.results);
        } finally {
            setloading(false)
        }
    }

    const [query, setquery] = useState("")

    return (
        <form className='search-bar' onSubmit={handlesearch}>
            <SearchIcon className='search-icon' size={22} />
            <input
                type="text"
                placeholder="Describe the movie you are looking for..."
                value={query}
                onChange={(e) => setquery(e.target.value)}
            />
            <button className='search-btn' type='submit'>
                <ArrowRight size={24} />
            </button>
        </form>
    )
}

export default Searchbar