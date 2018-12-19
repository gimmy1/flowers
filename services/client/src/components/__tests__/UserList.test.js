import React from 'react';
import {shallow} from 'enzyme';
import renderer from 'react-test-renderer';

import UsersList from '../UsersList';

const users = [
    {active: true, email: "gamal@gamal.com", id: 1, username: "gamal", admin: false},
    {active: true, email: "gimmy@mgimmy.com", id: 2, username: "gimmy", admin: false}
]

test('UsersList renders properly', () => {
    const wrapper = shallow(<UsersList users={users}/>);
    const element = wrapper.find('h4')
    const td = wrapper.find('tbody > tr > td')
    console.log(td.length)
    expect(td.length).toBe(10)
    // expect(wrapper.find('h1').get(0).props.children).toBe('All Users')
    // // expect(element.length).toBe(2)
    // expect(element.get(0).props.children).toBe('gamaZ')
})

test('UsersList renders a snapshot properly', () => {
    const tree = renderer.create(<UsersList users={users}/>).toJSON()
    expect(tree).toMatchSnapshot();
});