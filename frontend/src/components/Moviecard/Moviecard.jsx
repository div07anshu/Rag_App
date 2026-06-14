import React from "react";
import "./Moviecard.css";

import {
    Star,
    Calendar,
    Clock3,
    Clapperboard,
    Users,
    ThumbsUp,
    Sparkles,
} from "lucide-react";

const Moviecard = ({ movie }) => {
    return (
        <div className="movie-card">

            <div className="movie-poster">
                <img
                    src={movie.poster}
                    alt={movie.title}
                />
            </div>

            <div className="movie-content">
                <div className="movie-top">
                    <div>
                        <h2>{movie.title}</h2>

                        <div className="genres">
                            {movie.genres.map((genre, index) => (
                                <span
                                    key={index}
                                    className="genre-tag"
                                >
                                    {genre}
                                </span>
                            ))}
                        </div>
                    </div>

                    <div className="movie-rating">
                        <Star
                            size={18}
                            fill="currentColor"
                        />

                        <span>{movie.rating}</span>
                    </div>

                </div>

                <div className="movie-actors">
                    <Users size={18} />

                    <span>{movie.actor}</span>
                </div>

                <div className="movie-reason">

                    <div className="movie-reason-header">
                        <Sparkles size={18} />
                        <h4>
                            Why CineSage recommended this
                        </h4>

                    </div>

                    <p> {movie.reason || "This movie closely matches your query based on themes, genres, and semantic similarity."}</p>

                </div>

                <p className="movie-plot"> {movie.plot} </p>

                <div className="movie-footer">

                    <div className="movie-meta">
                        <Calendar size={16} />
                        {movie.year}
                    </div>

                    <div className="movie-meta">
                        <Clock3 size={16} />
                        {movie.runtime}
                    </div>

                    <div className="movie-meta">
                        <Clapperboard size={16} />
                        {movie.director}
                    </div>

                    <div className="movie-meta">
                        <ThumbsUp size={16} />
                        {movie.votes > 1000000
                            ? `${(movie.votes / 1000000).toFixed(1)}M`
                            : `${(movie.votes / 1000).toFixed(1)}K`
                        }
                    </div>

                </div>

            </div>

        </div>
    );
};

export default Moviecard;