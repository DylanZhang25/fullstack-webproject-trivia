import React, { Component } from 'react';
import $ from 'jquery';
import '../stylesheets/QuizView.css';

const questionsPerPlay = 5;

class QuizView extends Component {
  constructor(props) {
    super();
    this.state = {
      quizCategory: null,
      previousQuestions: [],
      showAnswer: false,
      categories: {},
      numCorrect: 0,
      currentQuestion: {},
      guess: '',
      forceEnd: false,
    };
  }

  componentDidMount() {
    $.ajax({
      url: `/categories`, //TODO1: update request URL
      type: 'GET',
      success: (result) => {
        this.setState({ categories: result.categories });
        return;
      },
      error: (error) => {
        alert('Unable to load categories. Please try your request again');
        return;
      },
    });
  }

  selectCategory = ({ type, id = 0 }) => {
    //as index of javascript array starts from 0, we need to add 1 to the id, beacuse the id of the category starts from 1
    const adjustedId = parseInt(id) + 1;
    // console.log('Selected Category:', adjustedId, type);
    this.setState({ quizCategory: { type, id:adjustedId } }, this.getNextQuestion);
  };

  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  };

  getNextQuestion = () => {

    const previousQuestions = [...this.state.previousQuestions];
    if (this.state.currentQuestion.id) {
      previousQuestions.push(this.state.currentQuestion.id);
    }
    // console.log("this.state.quizCategory: " + JSON.stringify(this.state.quizCategory));
    // console.log("previousQuestions: " + JSON.stringify(previousQuestions));
    $.ajax({
      url: '/quizzes', //TODO2: update request URL
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        previous_questions: previousQuestions,
        quiz_category: this.state.quizCategory
      }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          showAnswer: false,
          previousQuestions: previousQuestions,
          currentQuestion: result.question,
          guess: '',
          forceEnd: result.question ? false : true,
        });
        return;
      },
      error: (error) => {
        alert('Unable to load question. Please try your request again');
        return;
      },
    });
  };

  submitGuess = (event) => {
    event.preventDefault();
    let evaluate = this.evaluateAnswer();
    this.setState({
      numCorrect: !evaluate ? this.state.numCorrect : this.state.numCorrect + 1,
      showAnswer: true,
    });
  };

  restartGame = () => {
    this.setState({
      quizCategory: null,
      previousQuestions: [],
      showAnswer: false,
      numCorrect: 0,
      currentQuestion: {},
      guess: '',
      forceEnd: false,
    });
  };

  renderPrePlay() {
    return (
      <div className='quiz-play-holder'>
        <div className='choose-header'>Choose Category</div>
        <div className='category-holder'>
          <div className='play-category' onClick={this.selectCategory}>
            ALL
          </div>
          {Object.keys(this.state.categories).map((id) => {
            const category = this.state.categories[id].type;
            return (
              <div key={id} value={id} className='play-category' onClick={() => this.selectCategory({ type: category, id })}>
                {category}
              </div>
            );
          })}
        </div>
      </div>
    );
  }

  renderFinalScore() {
    return (
      <div className='quiz-play-holder'>
        <div className='final-header'>
          Your Final Score is {this.state.numCorrect}
        </div>
        <div className='play-again button' onClick={this.restartGame}>
          Play Again?
        </div>
      </div>
    );
  }

  evaluateAnswer = () => {
    const formatGuess = this.state.guess
      // eslint-disable-next-line
      .replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, '')
      .toLowerCase();
    const answerArray = this.state.currentQuestion.answer
      .toLowerCase()
      .split(' ');
    return answerArray.every((el) => formatGuess.includes(el));
  };

  renderCorrectAnswer() {
    let evaluate = this.evaluateAnswer();
    return (
      <div className='quiz-play-holder'>
        <div className='quiz-question'>
          {this.state.currentQuestion.question}
        </div>
        <div className={`${evaluate ? 'correct' : 'wrong'}`}>
          {evaluate ? 'You were correct!' : 'You were incorrect'}
        </div>
        <div className='quiz-answer'>{this.state.currentQuestion.answer}</div>
        <div className='next-question button' onClick={this.getNextQuestion}>
          {' '}
          Next Question{' '}
        </div>
      </div>
    );
  }

  renderPlay() {
    return this.state.previousQuestions.length === questionsPerPlay ||
      this.state.forceEnd ? (
      this.renderFinalScore()
    ) : this.state.showAnswer ? (
      this.renderCorrectAnswer()
    ) : (
      <div className='quiz-play-holder'>
        <div className='quiz-question'>
          {this.state.currentQuestion.question}
        </div>
        <form onSubmit={this.submitGuess}>
          <input type='text' name='guess' onChange={this.handleChange} />
          <input
            className='submit-guess button'
            type='submit'
            value='Submit Answer'
          />
        </form>
      </div>
    );
  }

  render() {
    return this.state.quizCategory ? this.renderPlay() : this.renderPrePlay();
  }
}

export default QuizView;
