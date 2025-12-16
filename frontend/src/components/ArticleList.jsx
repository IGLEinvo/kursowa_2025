import React from 'react';
import ArticleCard from './ArticleCard';
import './ArticleList.css';

const ArticleList = ({ articles, loading, error }) => {
  if (loading) {
    return <div className="loading">Loading articles...</div>;
  }

  if (error) {
    return <div className="error">Error loading articles: {error.message}</div>;
  }

  if (!articles || articles.length === 0) {
    return <div className="empty">No articles found.</div>;
  }

  return (
    <div className="article-list">
      {articles.map((article) => (
        <ArticleCard key={article.id} article={article} />
      ))}
    </div>
  );
};

export default ArticleList;




