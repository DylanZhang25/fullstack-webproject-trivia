import React, { Component } from 'react';
import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import $ from 'jquery';

class QuestionView extends Component {
  constructor() {
    super();
    this.state = {
      questions: [],
      page: 1,
      totalQuestions: 0,
      categories: {},
      currentCategory: null,
    };
  }

  componentDidMount() {
    this.getQuestions();
  }

  getQuestions = () => {
    $.ajax({
      url: `/questions?page=${this.state.page}`, //TODO1: update request URL
      type: 'GET',
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          categories: result.categories,
          currentCategory: result.current_category,
        });
        return;
      },
      error: (error) => {
        alert('getQuestions Unable to load questions. Please try your request again');
        return;
      },
    });
  };

  selectPage(num) {
    this.setState({ page: num }, () => this.getQuestions());
  }

  createPagination() {
    let pageNumbers = [];
    let maxPage = Math.ceil(this.state.totalQuestions / 10);
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === this.state.page ? 'active' : ''}`}
          onClick={() => {
            this.selectPage(i);
          }}
        >
          {i}
        </span>
      );
    }
    return pageNumbers;
  }

  getByCategory = (id) => {
    // index starts from 0 in the frontend categories list tab, so it should be increased by 1 and then sent to the backend
    // because the id of the category starts from 1 in the backend
    const categoryId = parseInt(id) + 1
    console.log("The selected id is: " + categoryId);
    $.ajax({
      url: `/categories/${categoryId}/questions`, //TODO2: update request URL
      type: 'GET',
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category,
        });
        return;
      },
      error: (error) => {
        alert('(getByCategory Unable to load questions. Please try your request again');
        return;
      },
    });
  };

  submitSearch = (searchTerm) => {
    $.ajax({
      url: `/questions/search`, //TODO3: update request URL (related to backend_TODO7, finished)
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({ searchTerm: searchTerm }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category,
        });
        return;
      },
      error: (error) => {
        alert('submitSearch Unable to load questions. Please try your request again');
        return;
      },
    });
  };

  questionAction = (id) => (action) => {
    if (action === 'DELETE') {
      if (window.confirm('are you sure you want to delete the question?')) {
        $.ajax({
          url: `/questions/${id}`, //TODO4: update request URL
          type: 'DELETE',
          success: (result) => {
            this.getQuestions();
          },
          error: (error) => {
            alert('questionAction Unable to load questions. Please try your request again');
            return;
          },
        });
      }
    }
  };

  render() {
    return (
      <div className='question-view'>
        <div className='categories-list'>
          <h2
            onClick={() => {
              this.getQuestions();
            }}
          >
            Categories
          </h2>
          <ul>
          {Object.keys(this.state.categories).map((id) => {
            const category = this.state.categories[id].type; 
            return (
              <li
                key={id}
                onClick={() => {
                  this.getByCategory(id);
                }}
              >
                {category}
                <img
                  className='category'
                  alt={`${category.toLowerCase()}`}
                  src={`${category.toLowerCase()}.svg`}
                />
              </li>
            );
          })}
          </ul>
          <Search submitSearch={this.submitSearch} />
        </div>
        <div className='questions-list'>
          <h2>Questions</h2>
          {this.state.questions.map((q, ind) => (
            <Question
              key={q.id}
              question={q.question}
              answer={q.answer}
              // category={this.state.categories[q.category]}
              /*
                I did a lot of research here and the provided code above is wrong. "this.state.categories[q.category]" will only return a undifined value.

                As QuestionView.js is the father of Question.js, when sending this prop to Question.js, the following line may error:
                  <img className='category' alt={`${category.toLowerCase()}`} src={`${category.toLowerCase()}.svg`}/>
                  TypeError: category.toLowerCase is not a function
                the type of "category" is undefined, which is not a string, so it doesn't have the function "toLowerCase". This error will affect the display of the category icon.

                One of the correct ways is the following code:
              */
              category={this.state.categories.find(cat => cat.id === q.category)?.type}
              difficulty={q.difficulty}
              questionAction={this.questionAction(q.id)}
            />
          ))}
          <div className='pagination-menu'>{this.createPagination()}</div>
        </div>
      </div>
    );
  }
}

export default QuestionView;
