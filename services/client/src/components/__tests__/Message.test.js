import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';

import Message from './Message'

describe('When given a success message', () => {
    const removeMessage = jest.fn()

    const messageSuccessProps = {
        messageName: 'Hello workd', 
        messageType: 'success',
        removeMessage: removeMessage
    }
    
    it('Message renders properly', () => {
        const wrapper = shallow(<Message {...messageSuccessProps} />);
        const element = wrapper.find('.notification.is-success');
        expect(element.length).toBe(1);
        const span = wrapper.find('span');
        expect(span.length).toBe(1);
        expect(span.get(0).props.children).toContain(
            messageSuccessProps.messageName)
        const button = wrapper.find('button')
        expect(button.length).toBe(1);
        expect(removeMessage).toHaveBeenCalled(0);
        button.simulate('click');
        expect(removeMessage).toHaveBeenCalled(1)
    })
    test('Message renders snapshot properly', () => {
        const tree = renderer.create(
            <Message {...messageSuccessProps}
        />).toJSON()
        expect(tree).toMatchSnapshot()
    })
})

describe('When given a danger message', () => {
    const removeMessage = jest.fn()

    const messageDangerProps = {
        messageName: 'Hello workd', 
        messageType: 'danger',
        removeMessage: removeMessage
    }

    it('Message renders properly', () => {
        const wrapper = shallow(<Message {...messageDangerProps}/>)
        const element = wrapper.find('.notification.is-danger')
        expect(element.length).toBe(1);
        const span = wrapper.find('span');
        expect(span.length).toBe(1);
        expect(span.get(0).props.children).toContain(
            messageSuccessProps.messageName)
        const button = wrapper.find('button')
        expect(button.length).toBe(1);
        expect(removeMessage).toHaveBeenCalled(0);
        button.simulate('click');
        expect(removeMessage).toHaveBeenCalled(1)
    })
    it('Message renders snapshot properly', () => {
        const tree = renderer.create(
            <Message {...messageDangerProps}
        />).toJSON()
        expect(tree).toMatchSnapshot()
    })
})