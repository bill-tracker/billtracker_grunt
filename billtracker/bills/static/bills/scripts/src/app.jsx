var React = require('react');
var ReactDOM = require('react-dom');
var classNames = require('classnames');

var AkomaNtosoHighlighter = React.createClass({
    render: function() {
        var rowClass = classNames('row');
        var colClass = classNames('col-sm-6');
        return <div className={rowClass}>
            <div className={colClass}>
                <h2>Insert Akoma Ntoso Document</h2>
                <textarea></textarea>
            </div>
            <div className={colClass}>
                <h2>Display Preview</h2>
            </div>
        </div>;
    }
});

ReactDOM.render(
  <AkomaNtosoHighlighter />,
  document.getElementById('app')
);