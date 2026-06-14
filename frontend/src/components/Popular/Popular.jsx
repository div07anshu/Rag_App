import React from 'react'
import "./Popular.css"
import { TrendingUpIcon } from 'lucide-react'

const searches = [
    "Nolan Movies",
    "Christopher Nolan sci-fi films",
    "Mind-bending thrillers",
    "Feel Good Movies",
    
]

const Popular = () => {
    return (
        <div className='popular'>
            <div className='popular-title'>
                <TrendingUpIcon size={20} />
                <h3>Popular Searches</h3>
            </div>
            <div className='search-tags'>
                {searches.map((search, index) => (
                    <button key={index} className='search-tag'>
                        {search}
                    </button>
                ))}
            </div>

        </div>
    )
}

export default Popular