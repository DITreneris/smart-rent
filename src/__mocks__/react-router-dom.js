const ReactRouterDOM = jest.requireActual('react-router-dom');

module.exports = {
  ...ReactRouterDOM,
  useNavigate: jest.fn().mockReturnValue(jest.fn()),
  useParams: jest.fn().mockReturnValue({}),
  useLocation: jest.fn().mockReturnValue({
    pathname: '/',
    search: '',
    hash: '',
    state: null
  }),
  Link: ({ children, to, ...rest }) => <a href={to} {...rest}>{children}</a>
}; 