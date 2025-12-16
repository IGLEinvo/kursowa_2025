import React from 'react';
import { Link } from 'react-router-dom';
import './ArticleCard.css';

const ArticleCard = ({ article }) => {
  const formatDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };

  return (
    <div className="article-card">
      {article.is_exclusive && (
        <span className="article-badge exclusive">Exclusive</span>
      )}
      <Link to={`/articles/${article.id}`} className="article-link">
        <h3 className="article-title">{article.title}</h3>
        {article.summary && (
          <p className="article-summary">{article.summary}</p>
        )}
        <div className="article-meta">
          <span className="article-date">
            {formatDate(article.published_at || article.created_at)}
          </span>
          <div className="article-stats">
            <span className="stat-item">👁 {article.views_count}</span>
            <span className="stat-item">❤️ {article.likes_count}</span>
            <span className="stat-item">💬 {article.comments_count}</span>
          </div>
        </div>
      </Link>
    </div>
  );
};

export default ArticleCard;




