import React from 'react';
import {shallow} from 'enzyme';
import renderer from 'react-test-renderer';

import UsersList from '../UsersList';

const users = [
    {active: true, email: "gamal@gamal.com", id: 1, username: "gamal"},
    {active: true, email: "gimmy@mgimmy.com", id: 2, username: "gimmy"}
]

test('UsersList renders properly', () => {
    const wrapper = shallow(<UsersList users={users}/>);
    const element = wrapper.find('h4')
    expect(element.length).toBe(2)
    expect(element.get(0).props.children).toBe('gamal')
})

test('UsersList renders a snapshot properly', () => {
    const tree = renderer.create(<UsersList users={users}/>).toJSON()
    expect(tree).toMatchSnapshot();
});