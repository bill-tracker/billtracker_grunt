var React = require('react');
var ReactDOM = require('react-dom');
var classNames = require('classnames');

var AkomaNtosoHighlighter = React.createClass({
    getInitialState: function() {
        return {
            value: '',
            color: 'red'
        };
    },
    componentDidMount: function(arg) { },
    handleChange: function(event) {
        this.setState({value: event.target.value});
    },
    render: function() {
        var rowClass = classNames('row');
        var colClass = classNames('col-sm-6');

        return <div className={rowClass}>
            <div className={colClass}>
                <h2>Insert Akoma Ntoso Document</h2>
                <textarea value={this.state.value} onChange={this.handleChange} />
            </div>
            <div className={colClass}>
                <h2>Display Preview</h2>
                {/*<div dangerouslySetInnerHTML={{__html: this.state.value}} />*/}
            </div>
        </div>;
    }
});

// TODO refactor this for more dynamic rendering...
ReactDOM.render(
  <AkomaNtosoHighlighter />,
  document.getElementById('app')
);