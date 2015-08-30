###############################################################################
#
# SageMathCloud: A collaborative web-based interface to Sage, IPython, LaTeX and the Terminal.
#
#    Copyright (C) 2015, William Stein
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

{rclass, flux, Flux, React, rtypes, FluxComponent} = require('flux')
{Col, Well, Button, Input, ButtonToolbar, ButtonInput} = require('react-bootstrap')
{Icon, Loading} = require('r_misc')
misc = require('misc')

WelcomeBack = rclass
    displayName : 'SignIn-WelcomeBack'

    render : ->
        <Col sm=6>
            <img src='favicon-128.png' width='64' height='64' className='img img-rounded' />
            <h2>Welcome back to SageMathCloud™!</h2>
        </Col>

AutomaticallySigningIn = rclass
    displayName : 'SignIn-AutomaticallySigningIn'

    render : ->
        <h3 style={color:'#666'}><Icon name='circle-o-notch' spin /> Signing in...</h3>

ForgotPassword = rclass
    displayName : 'SignIn-ForgotPassword'

    getInitialState : ->
        show : false

    show_forgot_password : (e) ->
        e.preventDefault()
        @setState(show : true)

    submit_forgot_password : (e) ->
        e.preventDefault()
        console.log('submit to', @refs.email.getValue())

    render : ->
        if not @state.show
            <div>
                <a href='' onClick={@show_forgot_password}>Forgot password?</a>
            </div>
        else
            <Well style={backgroundColor:'#fff'}>
                <h3>Forgot your password?</h3>
                <div>Enter your email address to reset your password.</div>
                <form onSubmit={@submit_forgot_password}>
                    <Input
                        ref         = 'email'
                        type        = 'email'
                        placeholder = 'Email address'
                        />
                    <ButtonToolbar>
                        <Button type='submit' bsStyle='primary' >
                            <Icon name='envelope-o' /> Send email
                        </Button>
                        <Button onClick={=>@setState(show : false)} >
                            Cancel
                        </Button>
                    </ButtonToolbar>
                </form>
            </Well>

SignInStrategies = rclass
    displayName : 'SignIn-Strategies'

    propTypes :
        strategies : rtypes.array

    componentDidMount : ->
        if not @props.strategies?
            @props.actions.set_sign_in_strategies()

    render_strategy : (name) ->
        if name is 'email'
            return
        <Button key={name} href={"/auth/#{name}"}>
            <Icon name={name} /> {misc.capitalize(name)}
        </Button>

    render : ->
        if not @props.strategies?
            return <Loading />
        <div>
            <hr />
            <h4>Or sign in using</h4>
            <ButtonToolbar bsSize='small'>
                {@render_strategy(name) for name in @props.strategies}
            </ButtonToolbar>
        </div>

SignInForm = rclass
    displayName : 'SignIn-Form'

    propTypes :
        strategies : rtypes.array
        actions    : rtypes.object # account actions

    render_sign_in_strategies : ->
        <SignInStrategies strategies={@props.strategies} actions={@props.actions} />

    sign_in : (e) ->
        e.preventDefault()
        email = @refs.email.getValue()
        password = @refs.password.getValue()
        @props.actions.sign_in(email, password)

    render : ->
        <div>
            <form onSubmit={@sign_in}>
                <h3>Sign in or create an account</h3>
                <Input ref='email' type='email' placeholder='Email' />
                <Input ref='password' type='password' placeholder='Password' />
                <Button type='submit' bsStyle='primary' style={marginBottom:'15px'} >
                    <Icon name='sign-in' /> Sign in
                </Button>
            </form>

            <ForgotPassword />

            {@render_sign_in_strategies() if @props.strategies?.length isnt 1}

            <hr />
            <span>Not working? Email us as <a target='_blank' href='mailto:help@sagemath.com'>help@sagemath.com</a> immediately!</span>
        </div>


SignIn = rclass
    displayName : 'SignIn'

    propTypes :
        strategies : rtypes.array
        flux       : rtypes.object

    render : ->
        account_actions = @props.flux.getActions('account')
        <div>
            <WelcomeBack />
            <Col sm=6>
                <Well>
                    <AutomaticallySigningIn />
                    <SignInForm strategies={@props.strategies} actions={account_actions} />
                </Well>
            </Col>
        </div>

render = () ->
    <FluxComponent flux={flux} connectToStores={'account'} >
        <SignIn />
    </FluxComponent>

React.render(render(), document.getElementById('smc-react-signin'))