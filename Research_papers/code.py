  \documentclass[journal]{IEEEtran}
\usepackage{amsmath}
\usepackage{amssymb}
%\usepackage[numbers,square,compress]{natbib}            % you should have natbib.sty

\usepackage{graphicx}          % Include this line if your 
                               % document contains figures,
\usepackage[dvips]{epsfig}    % or this line, depending on which
                               % you prefer.                         
                               
\usepackage{pgf}   
\usepackage{pgffor}
\usepackage{epstopdf}
\usepackage{verbatim}
\usepackage{multirow}
\usepackage{fancyhdr}
\usepackage{url}
\usepackage{amsthm}
\usepackage{siunitx}
\usepackage{algorithm}
\usepackage{algorithmic}
\newtheorem{theorem}{Theorem}
\newtheorem{lemma}[theorem]{Lemma}
\ifCLASSINFOpdf
 
% correct bad hyphenation here
\hyphenation{op-tical net-works semi-conduc-tor}

\begin{document}

\title{Target Guarding Problem under noisy measurements: Theory and Real Time Implementation
\thanks{ Naveen Kothuri, Jitesh Mohanan and Bharath Bhikkaji are with the Department of Electrical Engineering, Indian Institute of Technology Madras, India, 600036 (e-mail: jiteshnov1@gmail.com; bharath.bhikkaji@iitm.ac.in).}
}

\markboth{IEEE TRANSACTIONS ON CONTROL SYSTEM TECHNOLOGY}{Shell \MakeLowercase{\textit{et al.}}: Bare Demo of IEEEtran.cls for IEEE Journals}

\author{\IEEEauthorblockN{Naveen Kothuri, Jitesh Mohanan and Bharath Bhikkaji}
}

\maketitle

\begin{abstract}
The target guarding problem consists of two players, an evader and a pursuer. Evader tries to reach a stationary target while avoiding the pursuer, and the pursuer tries to intercept the evader before the target is attacked. Optimal strategies for the players have been studied extensively. These strategies assume the availability of perfect data (noise-free measurements of positions and speeds of the respective players are a common knowledge). Pursuer may lose an otherwise winning game due to lack of perfect data. In this work, it is investigated as to how the optimal strategies translate when noisy measurements of evader's position and speed are presented to the pursuer, while the evader has perfect information of pursuer's position and speed. Using the game geometry, a non-linear state space model is developed for the evader's maneuver. An Extended Kalman filter for this model is designed to estimate the evader's position and speed. A strategy based on the estimates is proposed for pursuer. Performance of this strategy is analyzed and also validated through experiments conducted on a test-bed consisting of mobile robots.   
%As the target guarding problem arises usually in building autonomous systems used in remote terrains, the measurement data is not always reliable. This study is important to do post-processing of the obtained measurement data before using it to make optimal decisions.  

\end{abstract}

\begin{IEEEkeywords}
Target protection games, Dominance regions, Apollonius circle,
Extended Kalman Filter, zero-sum difference games 
\end{IEEEkeywords}

\section{Introduction}
\IEEEPARstart{T}he Target Guarding Problem (TGP) or asset defending problem often finds applications in border security systems where autonomous robots are employed to guard a secluded territory of interest from intruders. In its basic form, first considered by Rufus Isaacs \cite{b1}, the TGP consists of two players, an evader \(E\)  and a pursuer \(P\), and also a stationary target \(T\) (Figure~\ref{fig:1}). The pursuer \(P\) guards the target \(T\) by trying to intercept \(E\) before \(E\) reaches \(T\). Simultaneously, \(E\) tries to reach \(T\) by evading the pursuer. %Pursuer wins the game if he successfully intercepts the evader before the evader reaches \(T\). Evader wins the game if he successfully evades pursuer and reaches \(T\). 
Assuming both $E$ and $P$  move with same speeds, Isaacs showed in \cite{b1}, that the optimal strategy for both the players is to head to the point on the perpendicular bisector of the line joining the instantaneous positions of both players, which is closest to the target zone. 

The case of the pursuer and the evader moving with unequal speeds was analyzed in \cite{b2}. When the speed of the evader is lesser than that of the pursuer, it was shown that the region of dominance of the evader on the play area was smaller than that of the pursuer, and that it was a circle (refereed to as the Apollonius circle) enclosing the evader (Figure~\ref{mpfig2}). In this case, the optimal path of both the players is to head to the point on the Apollonius circle, which is closest to the target zone. The optimal strategy was called the COIP law (Command to Optimal Interception Point) in \cite{b2}.


The strategies presented in \cite{b2} could not be implemented in real time due to the computational burden involved. This was worked upon in \cite{b11}, where the authors came up with a reformulated COIP law, which could be implemented in real time.

The optimal strategy of each player depends on the instantaneous position and speed of the other player. Thus, it is imperative that accurate position and speed measurements of one player are perfectly known to the other player to compute the optimal heading direction at each instant. The position and speed data of the players are usually captured via GPS, ultrasonic sensors or LIDARs and RADARs [Refs]. These sensors do present noisy data in many circumstances \cite{b21}, \cite{b22} .  Hence, cannot be relied upon to make decisions without post-processing their output. %The aim of this work is to derive a strategy for the pursuer when the measurements  of the evader position and speed  are corrupted by noise.  A non-linear model for the evader dynamics is  derived,  under the assumption that the evader plays optimally. An Extended Kalman Filter (EKF) \cite{b6} is designed for estimating the evader position and speed. This post-processed data is then acted upon by the pursuer to derive the best heading angle possible for the situation. 
This work attempts to derive a computable strategy for the pursuer in the TGP, when the evader data is noise corrupted. As part of this pursuit, the following contributions of this work are to be noted.

\begin{itemize}
    \item  A post-processing decision making algorithm (an Extended Kalman Filter) for the noisy measurements of evader's position and speed, enabling the pursuer to take decisions with respect to the instantaneous heading angle.
    \item Experimental verification of the pursuer strategy with noisy evader data, on a test bed consisting of mobile robots. 
\end{itemize}

This paper is organized as follows : Section~\ref{sec:Motivation} provides a brief survey on games similar to the TGP.  Section~\ref{sec:solution} presents existing solutions for the TGP in literature. In Section~\ref{sec:evader_man}, a dynamic model of the evader's maneuvers  is presented. Also, the corresponding extended Kalman filter application is explained. The proposed approach is validated on a generic test-bed consisting of mobile robots, and the associated implementation details are discussed in Sections~\ref{testbedsetup} and ~\ref{experimentalresults}.  The paper concludes with section~\ref{conclusion} which includes a brief on the scope of future work.

\section{The TGP: State of Art Solutions}
\label{sec:solution}

As mentioned in the introduction a TGP where both the players are assumed to have equal speeds  was considered in \cite{b1}.  If the target zone \(T\) is closer to the evader, the optimal strategy of evader is to employ pure-pursuit {\it i.e.,} head towards the target zone.  The pursuer loses in such a game. In general, the pursuer is closer to the target zone.  The locus of points that can be reached by both the pursuer and evader is the perpendicular bisector of the  line-joining their instantaneous positions,  Figure~ \ref{fig:1}.   The optimal strategy for both the players is to head towards \(D\), the point closest to \(T\) on the perpendicular bisector (refer Figure \ref{fig:1}(a)). In other words,  the optimal heading angles  $(\theta_p, \theta_e)$ for the pursuer and evader are
\begin{eqnarray}
\nonumber \theta_p &=&tan^{-1}\left(\frac{y_{I_n}-y_{p_n}}{x_{I_n}-x_{p_n}}\right)\\ 
\rm{and}
\label{head}
\\
\nonumber\theta_e &=& tan^{-1}\left(\frac{y_{I_n}-y_{e_n}}{x_{I_n}-x_{e_n}}\right)
\end{eqnarray}
respectively. The following argument, propounded in \cite{b1},  illustrates  this optimality. If the evader deviates from his optimal strategy while pursuer continues to play optimally, the interception would happen at a point farther than \(D\) from the target. This is shown in Figure \ref{fig:1}(b). As evader moves from \(E\) to \(E1\), then to \(E2\) and pursuer moves from \(P\) to \(P1\) to \(P2\), interception point $D$ shifts to \(D1\) and then to \(D2\) which are farther from \(T\) than \(D\). If the evader plays optimally, and the pursuer plays sub-optimally, the interception point moves closer to the target. This is shown in Figure \ref{fig:1}(c). As evader moves optimally from \(E\) to \(E1\) and pursuer moves sub-optimally from \(P\) to \(P1\), interception point $D$ shifts to \(D1\) which is closer to \(T\) than \(D\).
\begin{figure}[thpb]
	\centering
    \includegraphics[width=8cm,height=10cm]{Figures/Rufus.PNG}
	\caption{The Target Guarding Problem with Pursuer and Evader playing with equal velocities}
	\label{fig:1}
\end{figure}

The TGP with evader and pursuer having unequal speeds was considered in \cite{b2}. It was shown therein that the locus of points that can be reached by both the pursuer and evader in  equal time  is a circle  
 \begin{equation}
\label{capture circle}
(x-x_{c_n})^2+(y-y_{c_n})^2=R_{c_n}^2
\end{equation}
with center and radius being
\begin{equation*}
\begin{split}
x_{c_n}&=\frac{x_{e_n}-x_{p_n}k_{n}^2}{1-k_{n}^2}\ \ ,\ y_{c_n}=\frac{y_{e_n}-y_{p_n}k_{n}^2}{1-k_{n}^2}\\
R_{c_n}^2&=\frac{k_{n}^2}{(1-k_{n}^2)^2}((x_{e_n}-x_{p_n})^2+(y_{e_n}-y_{p_n})^2)
\end{split}
\end{equation*} 
respectively, where $k_n = \frac{V_e}{V_p}$ and Figure~\ref{mpfig2}.  As in equal velocity case, the optimal  strategy, for both players, is to find the instantaneous closest point $(x_{I_n},y_{I_n})$  to target on the capture locus and head towards it. An argument similar to the one presented for equal velocity case can be be propounded to establish the optimality of the strategy.  
\begin{figure}[thpb]
 \includegraphics[width=\linewidth]{Figures/pwin1.png}
	\caption{Game geometry when evader's speed is less than pursuer's speed}
	\label{mpfig2}
\end{figure} 

%It is to be emphasised here that the optimal heading angles for both the players depend on the instantaneous positions of either player, as given by (\ref{head}).



\section{Motivation and Related Work}
\label{sec:Motivation}

Most of the related literature has focused on Pursuit-Evasion (PE) games, where the pursuer tries to catch evader while the evader tries to escape. Analysis of such games can be found \cite{b19} and \cite{b20}, and more recently in \cite{b18}, \cite{b15}, \cite{b16} and \cite{b17}. In all these studies, the pursuer (or the team of pursuers) try to catch the evader (or the team of evaders) and the evader tries to escape from the pursuer. These games are akin to the classic cops-and-robbers game and the dynamics of the players are thus different from that of the target guarding problem.

Many solutions to stochastic PE games, where pursuer has imperfect measurements of evader's position and speed, have been proposed in literature. A PE game was formulated in a Bayesian game theoretic framework and an iterative algorithm was proposed in  \cite{b5}. Upper bounds on the expected capture time were found in \cite{b8}, \cite{b12}, \cite{b13} . But the fundamental roles of players in PE games are different from those of target guarding problem. Also, attempts to find strategies of players in stochastic version of TGP are not known (to the best of authors' knowledge). The approaches to solve for the  strategies of players in a general  stochastic pursuit-evasion game cannot be applied directly to the particular case of TGP, as both the games are completely different in terms of the objectives of the players. 

Dynamic target guarding problem ($i.e.,$ with a moving target), with the pursuer and evader having equal speeds , was considered in \cite{patcher2014}. Given the initial positions of players, critical speed of the target in order for the  pursuer to win the game was presented in \cite{patcher2014}. In \cite{b9}, a polygonal target region instead of a point was considered and optimal positioning of pursuer in order to minimize the area of vulnerability of target was determined. The TGP was formulated as linear quadratic optimization problem and optimal strategies  were derived in \cite{b10}. In all these works, the optimal strategies of the players were consistent with those provided in \cite{b1} and \cite{b2}.
\begin{comment}
Thus, there is no work in the present literature that analyses the TGP under noisy conditions and derives a reliable strategy for the pursuer that maximizes his chances of winning the game. Moreover, most of the work in literature is not optimized for real time implementations because of the inherent complexities of the derived solution.


In this work it is attempted to provide a reliable strategy for the pursuer to win the game when he receives noise-corrupted data of the evader's position and speed. This strategy is further successfully tested on a real time system employing mobile robots.

Here, it is assumed that the evader always gets perfect data of the position of pursuer and plays optimally at every instant whereas pursuer gets noise corrupted data of evader's position and speed. An Extended Kalman Filter (EKF) is designed for the dynamical model describing evader's maneuver. The performance of the EKF is studied through simulations and  is validated through experiments conducted on in-house test-bed developed.


\section{Problem Statement and Contributions}
\label{sec:statement}
It has been shown in \cite{b1} and \cite{b11}, that if the pursuer deviates from his optimal strategy for a sufficiently long time, it could be possible for the evader to win the game from an initially disadvantaged position. This can happen due to a multiple reasons and sensor measurement data corruption is one of the reasons. If the evader's position and speed measurements are noise corrupted, the pursuer obtains inaccurate data to operate upon. This results in an error in the calculation of the pursuer heading angle $\theta_{p}$ due to which, the pursuer path will be sub optimal. And could eventually enable the evader to win the game.


\begin{itemize}
\item 
This work attempts to derive a computable strategy for the pursuer in the TGP, when the evader data is noise corrupted. 
    \item  A post-processing decision making algorithm for the noisy measurements of evader's position and speed, enabling the pursuer to take decisions.
    \item Experimental verification of the pursuer strategy with noisy evader data, on a test bed consisting of mobile robots. 
\end{itemize}
\end{comment}
\section{Intercept Point motion analysis under suboptimal condition  }
\label{sec:evader_man}
Pursuer and evader move towards the interception point which remains stationary if both players play optimally. Under suboptimal condition interception moves.
\subsection{CASE 1:}
Lets assume only \(P\)  is playing suboptimal, therefore \(P\)  will not be heading towards intercept point(\(I\)). However, at each instant \(E\)  knows the current location of \(P\)  and moves toward that instantaneous interception point(\(I\)).

Let the mid point between \(P_1\) and \(E_1\) be \((x_{m1},y_{m1})\) and the slope of line joining \(P_1\) and \(E_1\) be \(M\) and the slope perpendicular to \(M\) be \(M_1\).
\begin{eqnarray}
x_{m1}&=&\frac{x_{e1}+x_{p1}}{2}
\label{xenext}
\\ y_{m1}&=&\frac{y_{e1}+y_{p1}}{2} 
\label{yenext}
\\ M&=&\frac{y_{e1}-y_{p1}}{x_{e1}-x_{p1}}
\label{venext}
\\ M_1&=&-\frac{x_{e1}-x_{p1}}{y_{e1}-y_{p1}}
\label{wenext}
\\ y-y_{m1}&=&M_1(x-x_{m1})
\end{eqnarray}
where the above line equation is line passing through \((x_{m1},y_{m1})\) having a slope perpendicular to \(M\). On simplifying the equation we get 
\begin{eqnarray}
L : (-M_1)x + y + (M_1x_{m1}-y_{m1}) = 0
\end{eqnarray}
The point on \(L\) closet to \(T\) is \(I\), which is 
\begin{eqnarray}
x_{i1}&=&\frac{c+M_1d+M_1(M_1x_{m1}-y_{m1})}{1+M_1^2}
\\ y_{i1}&=&\frac{M_1(c+M_1d)-(M_1x_{m1}-y_{m1})}{1+M_1^2}
\end{eqnarray}
Lets assume \(T\) to be at origin, Therefore 
\begin{eqnarray}
x_{i1}&=&\frac{M_1(M_1x_{m1}-y_{m1})}{1+M_1^2}
\\ y_{i1}&=&\frac{-(M_1x_{m1}-y_{m1})}{1+M_1^2}
\end{eqnarray}
substitute (3), (4) and (6) on (13) and (14),

\begin{eqnarray}
x_{i1} = \frac{-\frac{x_{e1}-x_{p1}}{y_{e1}-y_{p1}}(-\frac{x_{e1}-x_{p1}}{y_{e1}-y_{p1}}\frac{x_{e1}+x_{p1}}{2}-\frac{y_{e1}+y_{p1}}{2})}{1+(-\frac{x_{e1}-x_{p1}}{y_{e1}-y_{p1}})^2}
\end{eqnarray}
\begin{eqnarray}
x_{i1} = \frac{-\frac{x_{e1}-x_{p1}}{y_{e1}-y_{p1}}(-\frac{(x_{e1}-x_{p1})(x_{e1}+x_{p1})}{2(y_{e1}-y_{p1})}-\frac{(y_{e1}+y_{p1})(y_{e1}-y_{p1})}{2(y_{e1}-y_{p1})})}{1+(-\frac{x_{e1}-x_{p1}}{y_{e1}-y_{p1}})^2}
\end{eqnarray}
\begin{eqnarray}
x_{i1}&=&\frac{(x_{e1}-x_{p1})(x_{e1}^2-x_{p1}^2+ y_{e1}^2-y_{p1}^2)}{2((y_{e1}-y_{p1})^2+(x_{e1}-x_{p1})^2)}
\end{eqnarray}

\begin{eqnarray}
y_{i1} = \frac{-(-\frac{x_{e1}-x_{p1}}{y_{e1}-y_{p1}}\frac{x_{e1}+x_{p1}}{2}- \frac{y_{e1}+y_{p1}}{2})}{1+(-\frac{x_{e1}-x_{p1}}{y_{e1}-y_{p1}})^2}
\end{eqnarray}
\begin{eqnarray}
y_{i1} = \frac{-(-\frac{(x_{e1}-x_{p1})(x_{e1}+x_{p1})}{2(y_{e1}-y_{p1})}- \frac{(y_{e1}+y_{p1})(y_{e1}-y_{p1})}{2(y_{e1}-y_{p1})})}{1+(-\frac{x_{e1}-x_{p1}}{y_{e1}-y_{p1}})^2}
\end{eqnarray}
\begin{eqnarray}
y_{i1}&=&\frac{(y_{e1}-y_{p1})(x_{e1}^2-x_{p1}^2+ y_{e1}^2-y_{p1}^2)}{2((y_{e1}-y_{p1})^2+(x_{e1}-x_{p1})^2)}
\end{eqnarray}

Here let us consider \(A_1\) = \((x_{e1}^2-x_{p1}^2+ y_{e1}^2-y_{p1}^2)\) and \(D_1\) = \(2((y_{e1}-y_{p1})^2+(x_{e1}-x_{p1})^2)\), Therefore

\begin{eqnarray}
x_{i1}&=&\frac{(x_{e1}-x_{p1})(A_1)}{D_1}
\\ y_{i1}&=&\frac{(y_{e1}-y_{p1})(A_1)}{D_1}
\end{eqnarray}

In a small interval of time \(dt\), lets assume \(P\) moves from \(P_{1}(x_{p1},y_{p1})\) to \(P_{2}(x_{p2},y_{p2})\), \(E\) moves from \(E_{1}(x_{e1},y_{e1})\) moves to \(E_{2}(x_{e2},y_{e2})\), \(I\) moves from \(I_{1}(x_{i1},y_{i1})\) moves to \(I_{2}(x_{i2},y_{i2})\).Therefore the current \((x_{i2},y_{i2})\) with
\(T\) as origin are,
\begin{eqnarray}
x_{i2}&=&\frac{M_2(M_2x_{m2}-y_{m2})}{1+M_2^2}
\\ y_{i2}&=&\frac{M_1(M_2x_{m2}-y_{m2})}{1+M_2^2}
\end{eqnarray}
 in terms of \(A_2\) and \(D_2\), we can say that
\begin{eqnarray}
 x_{i2}&=&\frac{(x_{e2}-x_{p2})(A_2)}{D_2}
\\ y_{i2}&=&\frac{(y_{e2}-y_{p2})(A_2)}{D_2}
\end{eqnarray}

we know that \(P\) is playing suboptimal, therefore lets consider \(P\)'s heading angle be constant \(\alpha\). In a small time interval \(dt\), as \(E\) is playing optimal, \(E_1\) should he heading towards \(I_1\) and its instantaneous heading angle be \(x\), which is
\begin{eqnarray}
x&=&tan^{-1}\left(\frac{y_{e_1}-y_{p_1}}{x_{e_1}-x_{p_1}}\right) -tan^{-1}\left(\frac{y_{I_1}-y_{e_1}}{x_{I_1}-x_{e_1}}\right) 
\end{eqnarray}
on substituting equation (19) and (20) in (25), we get
\begin{eqnarray}
x=tan^{-1}\left(\frac{y_{e_1}-y_{p_1}}{x_{e_1}-x_{p_1}}\right) -tan^{-1}\left(\frac{y_{e1}(A_1-D_1)-y_{p1}A_1}{x_{e1}(A_1-D_1)-x_{p1}A_1}\right)
\end{eqnarray}
the \(\alpha\) and \(x\) are absolute angles taken with respect to line joining instantaneous \(P\) and \(E\).

We are considering the case where \(P\) and \(E\) moves with same speed \(v\), therefore in that small interval of time \(dt\)
\begin{eqnarray}
x_{p2}&=&x_{p1} + vdtcos(\alpha)
\\ y_{p2}&=&y_{p1} + vdtsin(\alpha)
\\ x_{e2}&=&x_{e1} + vdtcos(x)
\\ y_{e2}&=&y_{e1} + vdtsin(x)
\end{eqnarray}
From the above expression lets assume that \(q = vdtcos(\alpha)\), \(r = vdtsin(\alpha)\), \(s = vdt(cosx)\), \(t = vdt(sinx)\), therefore
\begin{eqnarray}
x_{p2}&=&x_{p1} + q
\\ y_{p2}&=&y_{p1} + r
\\ x_{e2}&=&x_{e1} + s
\\ y_{e2}&=&y_{e1} + t
\end{eqnarray}
substitute (31),(32),(33) and (34) in \(A2\)
\begin{eqnarray}
A_2 &=& (x_{e2}^2-x_{p2}^2+ y_{e2}^2-y_{p2}^2)
\end{eqnarray}
\begin{equation}
\begin{aligned}
A_2 ={} & \{(x_{e1} + s)^2 - (x_{p1} + q)^2\\
        & + (y_{e1} + t)^2 - (y_{p1} + r)^2 \}     
\\ A_2 ={} & \{ (x_{e1}^2 + s^2 + 2x_{e1}s) - (x_{p1}^2 + q^2 + 2x_{p1}q)\\
        & + (y_{e1}^2 + t^2 + 2y_{e1}t)- (y_{p1}^2 + r^2 + 2y_{p1}r) \}
\\ A_2 ={} & \{ (x_{e1}^2 + 2x_{e1}s) - (x_{p1}^2 + 2x_{p1}q)\\
           & + (y_{e1}^2 + 2y_{e1}t)- (y_{p1}^2 + 2y_{p1}r) \}
\\ A_2 ={} & \{x_{e1}^2 - x_{p1}^2 + y_{e1}^2 - y_{p1}^2\\   
           & + 2x_{e1}s - 2x_{p1}q + 2y_{e1}t) - 2y_{p1}r \}
\end{aligned}
\end{equation}
where \(q^2,r^2,s^2,t^2\) are in the form \(dt^2\), which is approximately equal to \(0\) which can be neglected from the above equation (36).
\begin{eqnarray}
A_2 = A_1 + 2(x_{e1}s - x_{p1}q + y_{e1}t - y_{p1}r) 
\end{eqnarray}
substitute (31),(32),(33) and (34) in \(A2\)
\begin{eqnarray}
D_2 &=& 2((y_{e2}-y_{p2})^2+(x_{e2}-x_{p2})^2)
\end{eqnarray} 
\begin{equation}
\begin{aligned}
D_2 ={} & \{2(y_{e2}^2 + y_{p2}^2 -  2y_{p2}y_{e2}\\
        & + x_{e2}^2 + x_{p2}^2 -  2x_{p2}x_{e2})\}     
\\ (y_{p2}y_{e2} ={} & \{ (y_{e1} + t)(y_{p1} + r)\})
\\ y_{p2}y_{e2} ={} & \{ y_{e1}y_{p1}+(y_{e1}r+ y_{p1}t +rt) \}
\\ (x_{p2}x_{e2} ={} & \{ (x_{e1} + s)(x_{p1} + q)\}
\\ x_{p2}x_{e2} ={} & \{ x_{e1}x_{p1}+(x_{e1}q+ x_{p1}s +sq) \})
\\ D_2 ={} & \{ 2((y_{e1}^2 + 2y_{e1}t) + (y_{p1}^2 + 2y_{p1}r) \\
           & -2(y_{e1}y_{p1}+y_{e1}r+ y_{p1}t +rt)\\
           & + (x_{e1}^2 + 2x_{e1}s) + (x_{p1}^2 + 2x_{p1}q) \\
           & -2(x_{e1}x_{p1}+x_{e1}q+ x_{p1}s +sq)) \}
\\ D_2 ={} & \{ 2((y_{e1}^2 + y_{p1}^2 -2(y_{e1}y_{p1})) \\
           & + (x_{e1}^2 + x_{p1}^2 -2(x_{e1}x_{p1}))\\
           & + 2y_{e1}t + 2y_{p1}r - 2y_{e1}r - 2y_{p1}t \\
           & + 2x_{e1}s + 2x_{p1}q - 2x_{e1}q - 2x_{p1}s \}
\\ D_2 ={} & \{ 2((y_{e1}-y_{p1})^2+(x_{e1}-x_{p1})^2) \\
           & + 4(y_{e1}(t-r) - y_{p1}(t-r) \\
           & + x_{e1}(s-q) - x_{p1}(s-q)) \}
\end{aligned}
\end{equation}
where \(sq,rt\) are in the form \(dt^2\), which is approximately equal to \(0\) which can be neglected from the above equation (39).
\begin{eqnarray}
D_2 = D_1 + 4((y_{e1}-y_{p1})(t-r)+ (x_{e1}- x_{p1})(s-q)) 
\end{eqnarray} 

On expanding \(I_{2}(x_{i2},y_{i2})\) in terms of \(P_1\),\(E_1\),\(\alpha\),\(x\),
\begin{eqnarray}
\begin{aligned}
x_{i2} = \frac{(x_{e2}-x_{p2})(A_2)}{D_2}
\\ x_{i2} = \frac{((x_{e1}+s)-(x_{p1}+q))(A_2)}{D_2}
\\ x_{i2} = \frac{(x_{e1}-x_{p1})A_2+(s-q)(A_2)}{D_2}
\\ x_{i2} = \frac{(x_{e1}-x_{p1})A_2+(s-q)(A_1)}{D_2} 
\end{aligned}
\end{eqnarray}
where \((s-q)(x_{e1}s - x_{p1}q + y_{e1}t - y_{p1}r)\) is in the form \(dt^2\), which is approximately equal to \(0\) which can be neglected from the above equation (41).
\begin{eqnarray}
\begin{aligned}
similarly : y_{i2} = \frac{(y_{e1}-y_{p1})A_2+(t-r)(A_1)}{D_2} 
\end{aligned}
\end{eqnarray}

In that small interval \(dt\), we are interested in \(dx_i\) and \(dy_i\)
\begin{eqnarray}
\begin{aligned}
dx_i &= x_{i2} - x_{i1}
\\ dx_i = {} & \{ \frac{(x_{e1}-x_{p1})A_2+(s-q)(A_1)}{D_2} \\ 
          & -\frac{(x_{e1}-x_{p1})(A_1)}{D_1} \}
\\ dx_i &= \frac{(x_{e1}-x_{p1})(D_1A_2-D_2A_1)+(s-q)A_1D_1}{D_1D_2}        
\\ dy_i &= y_{i2} - y_{i1}
\\ dy_i = {} & \{ \frac{(y_{e1}-y_{p1})A_2+(t-r)(A_1)}{D_2} \\ 
          & -\frac{(y_{e1}-y_{p1})(A_1)}{D_1} \}
\\ dy_i &= \frac{(y_{e1}-y_{p1})(D_1A_2-D_2A_1)+(t-r)A_1D_1}{D_1D_2}
\end{aligned}
\end{eqnarray}

From this we can derive instantaneous slope, x and y components of speeds.
\begin{eqnarray}
\begin{aligned}
\frac{dy_i}{dx_i}&= \frac{(y_{e1}-y_{p1})(D_1A_2-D_2A_1)+(t-r)A_1D_1}{(x_{e1}-x_{p1})(D_1A_2-D_2A_1)+(s-q)A_1D_1} \\
\frac{dx_i}{dt} &= \frac{(x_{e1}-x_{p1})(D_1A_2-D_2A_1)+(s-q)A_1D_1}{(D_1D_2)dt} \\
\frac{dy_i}{dt} &= \frac{(y_{e1}-y_{p1})(D_1A_2-D_2A_1)+(t-r)A_1D_1}{(D_1D_2)dt}
\end{aligned}
\end{eqnarray}

\subsection{CASE 2:}
Now lets assume only \(E\)  is playing suboptimal, therefore \(E\)  will not be heading towards intercept point(\(I\)). However, at each instant \(P\)  knows the current location of \(E\)  and moves toward that instantaneous interception point(\(I\)).

This case is similar to the one above solved and here we know that \(E\) is playing suboptimal, therefore lets consider \(E\)'s heading angle be constant \(\alpha\). In a small time interval \(dt\), as \(P\) is playing optimal, \(P_1\) should he heading towards \(I_1\) and its instantaneous heading angle be \(x\), which is
\begin{eqnarray}
x&=&tan^{-1}\left(\frac{y_{e_1}-y_{p_1}}{x_{e_1}-x_{p_1}}\right) -tan^{-1}\left(\frac{y_{I_1}-y_{p_1}}{x_{I_1}-x_{p_1}}\right) 
\end{eqnarray}
on substituting equation (19) and (20) in (25), we get
\begin{eqnarray}
x=tan^{-1}\left(\frac{y_{p_1}-y_{e_1}}{x_{p_1}-x_{e_1}}\right) -tan^{-1}\left(\frac{y_{p1}(A_1-D_1)-y_{e1}A_1}{x_{p1}(A_1-D_1)-x_{e1}A_1}\right)
\end{eqnarray}
the \(\alpha\) and \(x\) are absolute angles taken with respect to line joining instantaneous \(P\) and \(E\).

We are considering the case where \(P\) and \(E\) moves with same speed \(v\), therefore in that small interval of time \(dt\)
\begin{eqnarray}
x_{p2}&=&x_{p1} + vdtcos(x)
\\ y_{p2}&=&y_{p1} + vdtsin(x)
\\ x_{e2}&=&x_{e1} + vdtcos(\alpha)
\\ y_{e2}&=&y_{e1} + vdtsin(\alpha)
\end{eqnarray}
From the above expression lets assume that \(q = vdtcos(x)\), \(r = vdtsin(x)\), \(s = vdt(\alpha)\), \(t = vdt(\alpha)\), therefore
\begin{eqnarray}
x_{p2}&=&x_{p1} + q
\\ y_{p2}&=&y_{p1} + r
\\ x_{e2}&=&x_{e1} + s
\\ y_{e2}&=&y_{e1} + t
\end{eqnarray}
The instantaneous points \(I_{1}(x_{i1},y_{i1})\) and \(I_{2}(x_{i2},y_{i2})\) are
\begin{eqnarray}
x_{i1}&=&\frac{(x_{p1}-x_{e1})(A_1)}{D_1} \\
y_{i1}&=&\frac{(y_{p1}-y_{e1})(A_1)}{D_1} \\
x_{i2}&=&\frac{(x_{p2}-x_{e2})(A_2)}{D_2} \\
&=&\frac{(x_{p1}-x_{e1})A_2+(q-s)(A_1)}{D_2} \\
y_{i2}&=&\frac{(y_{p2}-y_{e2})(A_2)}{D_2} \\
&=&\frac{(y_{p1}-y_{e1})A_2+(r-t)(A_1)}{D_2}
\end{eqnarray}
where,
\begin{eqnarray}
A_1&=&(x_{p1}^2-x_{e1}^2+ y_{p1}^2-y_{e1}^2)\\
D_1&=&2((y_{p1}-y_{e1})^2+(x_{p1}-x_{e1})^2)\\
A_2&=&A_1 + 2(x_{p1}q - x_{e1}s + y_{p1}r - y_{e1}t )\\
D_2&=&D_1 + 4((y_{p1}-y_{e1})(r-t)+ (x_{p1}- x_{e1})(q-s))
\end{eqnarray}

From this we derived instantaneous slope, x and y components of speeds.
\begin{eqnarray}
\begin{aligned}
\frac{dy_i}{dx_i}&= \frac{(y_{p1}-y_{e1})(D_1A_2-D_2A_1)+(r-t)A_1D_1}{(x_{p1}-x_{e1})(D_1A_2-D_2A_1)+(q-s)A_1D_1} \\
\frac{dx_i}{dt} &= \frac{(x_{p1}-x_{e1})(D_1A_2-D_2A_1)+(q-s)A_1D_1}{(D_1D_2)dt} \\
\frac{dy_i}{dt} &= \frac{(y_{p1}-y_{e1})(D_1A_2-D_2A_1)+(r-t)A_1D_1}{(D_1D_2)dt}
\end{aligned}
\end{eqnarray}

\subsection{ANALYSIS:}
\subsubsection{Analysis 1}
The equation (44) also satisfy the optimal play also, because in optimal play \(\alpha\) = \(x\) and we know that intercept point will not be moving, this implies \(I_1\) and \(I_2\) are equal. As \(\alpha\) = \(x\), therefore \((r-t)= (q-s) = 0\) and  \(I_1\) = \(I_2\), on substituting \((q-s) = 0\), we get \(D_1 = D_2\)and equating  \(x_{i1}\) = \(x_{i2}\), we get 
\begin{eqnarray}
\frac{A_1}{D_1}&=&\frac{A_2}{D_2} \\
A_1D_2 - A_2D_1&=&0 \\
also: D_1&=&D_2,therefore A_1=A_2 \\
implies: 0&=&s(x_{e1} - x_{p1}) + t(y_{e1} - y_{p1})  
\end{eqnarray}
\subsubsection{Analysis 2}
When \((x_{e1}-x_{p1})\) tends to \(0\),therefore on substituting in equation (44) we get,
\begin{eqnarray}
\frac{dx_i}{dt} &=& \frac{(q-s)A_1D_1}{(D_1D_2)dt} \\
&=& \frac{(q-s)A_1}{D_2dt} \\
&=& \frac{(q-s)A_1}{D_1dt} \\
&=& \frac{(q-s)A_1}{((y_{p1}-y_{e1})^2)dt}
\end{eqnarray}
where \(dt(4((y_{e1}-y_{p1})(t-r)+ (x_{e1}- x_{p1})(s-q)))\) is in the form \(dt^2\), which is approximately equal to \(0\) which can be neglected from the above equation (69).

From the equation (71), we can say that\((y_{e1}-y_{p1})\) tends to \(\infty\) the systems acts more optimal along \(X_{axis}\) and when \((y_{e1}-y_{p1})\) tends to \(0\) the systems acts more optimal along \(Y_{axis}\). Under suboptimal condition, whenever it plays more optimal along one axis then it's eventually playing more suboptimal along the other axis.

Therefore we can conclude that \((\alpha - x)\) decides how much optimally the game is being played and under the assumption when \((x_{e1}-x_{p1})\) tends to \(0\), \((y_{e1}-y_{p1})\) decides how much optimally the game is being played with respect to \(X_{axis}\) and \(Y_{axis}\).
\subsubsection{Analysis 3}: When both \(P\) and  \(E\) head at same suboptimal angle we get \((r-t)= (q-s) = 0\), therefore using this condition on\((x_{i1}\) and \(x_{i2})\) and on substituting equation (69) ,we get \(dx_i=0\) and similarly 
\(dx_i=0\). This proves that theoretically when both \(P\) and  \(E\) head at same suboptimal angle, the intercept point \(I\) will not move.




\subsection{EKF to estimate position and speed of evader}
The algorithm of EKF \cite{b6} is shown in Algorithm. 1. The computational ease of the Kalman filter is because of the brevity of its algorithm which allows for its use in many real world estimation problems including the problem under consideration.
\begin{algorithm}
\begin{algorithmic}
\label{algortihm}
\STATE \textbf{Initialization:}
\STATE  $\hat{X}_{0|0}=C^{-1}Z_0,$
\\ \textit{LOOP Process}
\STATE \textbf{Prediction:}
\STATE $\hat{X}_{n|n-1}=f(\hat{X}_{n-1|n-1},u_n)$
\STATE $P_{n|n-1}=A_nP_{n-1|n-1}A_n^T + Q$
\STATE Measurement residual: \ \ 	$\tilde {y}_{n}={Z}_{n}-h(\hat {X}_{n|n-1}) $
\STATE  Near-optimal Kalman gain:\\ \hspace{2.6cm} $\hat{K}_{n}=P_{n|n-1}C^T(CP_{n|n-1}C^T+R)^{-1}$
\STATE \textbf{Correction:}
\STATE $\hat{X}_{n|n}=\hat{X}_{n|n-1}+K_{n}\tilde {y}_{n}$
\STATE $P_{n|n}=(I-K_{n}C^T)P_{n|n-1}$
\STATE \textbf{goto} \emph{loop}.
\STATE \textbf{close};
\end{algorithmic}
\end{algorithm}

where \(\hat{X}_{a|b}\) is the estimate of state vector at time instant \(a\)' based on measurements available at time instant '\(b\)', \(f=[G\ H\ V]^T\) and \(u_n\) is the input vector. 
\begin{equation}
\begin{split}
A_n &= \left(\begin{array}{ccc}
\frac{\partial G}{\partial x_e} & \frac{\partial G}{\partial y_e} & \frac{\partial G}{\partial k_e}\\
\\\frac{\partial H}{\partial x_e} & \frac{\partial H}{\partial y_e} & \frac{\partial H}{\partial k_e}\\
\\\frac{\partial L}{\partial x_e} & \frac{\partial L}{\partial y_e} & \frac{\partial L}{\partial k_e}
\end{array}\right)\\ &= \left(\begin{array}{ccc}
\frac{\partial G}{\partial x_e} & \frac{\partial G}{\partial y_e} & \frac{\partial G}{\partial k_e}\\
\\ \frac{\partial H}{\partial x_e} & \frac{\partial H}{\partial y_e} & \frac{\partial H}{\partial k_e}\\
\\0 & 0 & 1
\end{array}\right)_{(\hat{x}_{e_{n|n}},\hat{y}_{e_{n|n}},\hat{V}_{{n|n}},x_{p_{n}},y_{p_{n}})}
\end{split}
\end{equation}

Note that linearization operation is performed after substituting (\ref{fx}), (\ref{fy}) in (\ref{xenext}) and (\ref{yenext}).


\subsection{Condition to check if evader has won the game}

For evader to win the game, target has to be inside evader's dominance region. Therefore,
\begin{equation}
\label{targetcircle}
(x_T-x_{c})^2+(y_T-y_{c})^2 \leq R_{c}^2
\end{equation}
Substituting expressions for center and radius of Apollonius circle, we get the following inequality. 
\begin{equation}
\begin{split}
(x-x_T)^2+(y-y_T)^2 \leq k^2((x_{p_n}-x_T)^2+(y_{p_n}-y_T)^2)
\end{split}
\end{equation}
where \(k=\frac{V}{V_p}\) is ratio of speeds of evader and pursuer. \((x,y)\) is position of evader. Denote the radius of the circle by \(R_{T_n}\).
This implies  \[\frac{(x-x_T)^2+(y-y_T)^2}{V^2} \leq \frac{(x_p-x_T)^2+(y_p-y_T)^2}{V_p^2}\] .

So the locus of all evader positions for which target is the interception point is a circle with center \((x_T,y_T)\).  

So if distance between target and evader is smaller than \(R_{T_n}\) then target will be in the dominance region of evader.

Kalman filter produces the estimates of mean and state error covariance values of \(x_e, y_e, V\). Using the estimated speed of evader, \(V\), the set of all evader positions whose interception point coincides with the target can be found.  Denote the circle by \(C_{\hat{V}}\)  

Consider a rectangle \(\mathcal{R}\) with length and breadth equal to 
\(6\hat{\sigma}_x,6\hat{\sigma}_y\). Let the center of this rectangle be at \(\hat{x}_{e_{n|n}}, \hat{y}_{e_{n|n}}\).

The following condition is used to check if target is in evader's dominance region 
\begin{equation}
\sqrt{(3\hat{\sigma}_x)^2+(3\hat{\sigma}_y)^2} + R_{T_n} \leq \sqrt{(x_T-\hat{x}_{e_{n|n}})^2+(y_T-\hat{y}_{e_{n|n}})^2} 
\end{equation}

This condition means that if \(\mathcal{R}\) and \(C_{\hat{V}}\) intersect, then there is non-zero probability that pursuer has lost the game. As the game progresses, \(\hat{\sigma}_x, \hat{\sigma}_y\) converge to zero and estimates of to the actual speed of evader, we can check this condition to find if evader has won the game. Evader wins the game if \(\mathcal{R}\) is inside \(C_{\hat{V}}\).

\subsection{Simulation results:}
%As the system is non-linear, it is through simulations alone, the performance of the Kalman observer can be analyzed. Also as the location of target is independent of pursuer's location, pursuer may fail to protect the target because of his sub-optimal play if he is not close to the target. System is found to be weakly observable \textit{i.e.,} as \(rank(A_n)\) is found out to be equal to 3 for the entire duration of game.

Simulation results of a game with the following statistics are presented.

Let \(T\) be target, \(I_0, I_f\) be initial and final interception points. Final interception point is calculated when pursuer reaches within specified distance \(D\) from the evader.
 The performance index, \(P.I\) of optimality of pursuer's path when measurements are corrupted by noise is given by (\ref{PI}).
 \begin{equation}
 \label{PI}
 P.I=\frac{Dist(T,I_f)}{Dist(T,I_0)}
 \end{equation}
 where \(Dist(a,b)\) is the distance between the points \(a\) and \(b\)
 
 In deterministic case where perfect measurements of evader's position and speed are available to pursuer, \(P.I=1\). 
 
 
\begin{table}[h]
\begin{tabular}
{|c|c|c|}
\hline
\((x_{p_0},y_{p_0}),V_p\) & (105,85), 10 \\
\hline
\((x_{e_0},y_{e_0}), V\) & (50,60), 7 \\
\hline
\((x_T,y_T), \Delta T\) & (100,40), 0.1 \\
\hline
Diagonal elements of \(R\) & (64,64,1.5)\\
\hline
diagonal elements of \(Q\)& (10,10,0)\\
\hline
diagonal elements of \(P_0\)& (64,64,1.5)\\
\hline
\(Dist(T,I_0)\) & 19.9952\\
\hline
\(Dist(T,I_f)\) & 19.6919\\
\hline
\(P.I\) & 0.9848\\
\hline
\end{tabular}
\end{table}
\begin{figure}[thbp]
    \includegraphics[width=9cm]{Figures/game1.eps}\caption{Plot of pursuer's and evader's paths}\label{game1kf1}
\end{figure}
\begin{comment}
\begin{figure}[thbp]
    \includegraphics[width=9cm]{Figures/game2.eps}
\caption{Plot with noise variance \(3\sigma_x^2,3\sigma_y^2,3\sigma_v^2\)}\label{game2kf1}
\end{figure}
\end{comment}

Paths followed by pursuer and evader are shown in Figures \ref{game1kf1}. The final interception point is approximately at same distance from the target as the initial interception point which implies pursuer has played nearly optimally.

Auto-covariances of states \(x_e, y_e\) reached non-zero steady state values (approximately equal to process noise variance values of the states) approximately after \(n=7\) (refer Figure  \ref{speed2kf1}). However, the auto-covariance of the state \(V\) settled only after \(n=15\) which means Kalman filter improved the estimate of \(V\) using measurements until \(n=15\) and so the estimate of \(V\) converged to true value.
\begin{comment}
\begin{figure}[!tbp]
  \begin{minipage}[b]{0.4\textwidth}
    \includegraphics[width=8cm]{Figures/speed1.eps}
    \begin{center}
    \caption{Plots of measured, estimated, true speed of evader when measurement noise variance is \(\sigma_x^2,\sigma_y^2,\sigma_v^2\)}\label{speed2kf1}
      \end{center}
  \end{minipage}
  \hfill
  \begin{minipage}[b]{0.4\textwidth}
    \includegraphics[width=8cm]{Figures/speed2.eps}
    \begin{center}
    \caption{Plots of measured, estimated, true speed of evader when measurement noise variance is \(3\sigma_x^2,3\sigma_y^2,3\sigma_v^2\)}\label{speed1kf1}
      \end{center}
  \end{minipage}
\end{figure}
\end{comment}
\begin{figure}
\includegraphics[width=8cm]{Figures/speed1.eps}\caption{Plots of measured, estimated, true speed of evader}\label{speed2kf1}
\end{figure}
\begin{figure}
\includegraphics[width=8cm]{Figures/variance.eps}
\caption{Plots of auto-covariances of states}
\end{figure}
\begin{comment}
\begin{figure}
\hspace{.6cm}
\includegraphics[width=8cm]{Figures/speed1.eps}
\caption{Plots of measured, estimated, true speed of evader}\label{speed2kf1}
\end{figure}

\begin{figure}[!tbp]
  \begin{minipage}[b]{0.4\textwidth}
    \includegraphics[width=9cm]{Figures/variance.eps}
    \begin{center}
    \caption{Auto covariance plots of states when measurement noise variance is \(\sigma_x^2,\sigma_y^2,\sigma_v^2\)}
    \label{variance1kf1}
      \end{center}
  \end{minipage}
  \hfill
  \begin{minipage}[b]{0.4\textwidth}
    \includegraphics[width=9cm]{Figures/variance2.eps}
   \begin{center}
    \caption{Auto covariance plots of states when measurement noise variance is \(3\sigma_x^2,3\sigma_y^2,3\sigma_v^2\)}     \label{variance2kf1}
      \end{center}
  \end{minipage}
\end{figure}
\begin{figure}
\includegraphics[width=9cm]{Figures/variance.eps}
\caption{Auto covariance plots of states}
    \label{variance1kf1}
\end{figure}
\end{comment}
\begin{figure}[!tbp] \includegraphics[width=8.5cm]{Figures/evaderpositions1.eps}
    \caption{Plots to show estimates of position of evader. Note that estimates are not converging onto true position because of non-zero process noise}\label{gamea1kf1}
    \end{figure}
\begin{figure}[thpb]    
\includegraphics[width=8.4cm]{Figures/game3.eps}
	\caption{Evader wins the game as initial position of pursuer is far from the target.}\label{evaderwin}
\end{figure}

    \begin{comment}
        \begin{figure}
    \includegraphics[width=9.1cm]{Figures/evaderpositions2.eps}	
    \label{gamea2f1}
  \caption{Plots to show estimates of position of evader when measurement noise variance is \(3\sigma_x^2,3\sigma_y^2,3\sigma_k^2\)}
\end{figure}
    \end{comment}

Plot \ref{evaderwin} presents a game where target is close to initial interception point. By the time pursuer is within \(D\) units distance from evader, target is in evader's dominance region. Evader wins the game. This is because pursuer's initial position is far from the target and so pursuer, owing to his sub-optimal play,  couldn't get enough time to protect the target. When measurement data is associated with noise, pursuer wins the game only if he is close to the target at the beginning of the game.


\section{A test bed for implementing control laws in a two player difference game}
\label{testbedsetup}
 The platform consists of two LEGO EV3 robots and a ceiling mounted motion capture system to detect the player's co-ordinates. Each LEGO robot has a differential drive system with PID controllers for  the drive motors which precisely control the motion of the robot. The control law is run in  Matlab and the desired position and yaw angle of the robots are calculated. Gaussian noise is added to the acquired measurement data to simulate conditions of noisy measurement.
\begin{figure}[thpb]
\hspace{-1cm}
\includegraphics[width=10cm]{Figures/motive1.png}
	\caption{Block diagram showing how the position and yaw angle of robot are controlled}
	\label{motive}
\end{figure}

Figure \ref{motive} depicts how  control commands are communicated to robot to achieve the desired position and orientation. Placement of markers is shown in Figure \ref{robots}. 
\begin{figure}[thpb]\includegraphics[width=8cm]{Figures/robots.png}
	\caption{Markers are placed asymmetrically on each of the two robots to distinguish one from the other}\label{robots}
\end{figure}


\subsection{Practical considerations}
\label{implementationdifficulties}
So far, in devising strategies for the pursuer to win the game in-spite of the unavailability of perfect information of evader's position and speed, it has been assumed that both the players are point robots with infinite turn rate. These assumptions do not hold true in real time and so the optimal strategies are affected by size and turn rate of players. The time taken for the robot to align in the instantaneous optimal heading angle direction affects the overall performance of the player. Also while turning, the translation speed of the robot need not be zero. After the robot aligns in  the optimal heading angle direction, the position of the robot changes and heading angle of the robot need not be optimal with respect to its new position. These two non-ideal considerations can be modeled as Gaussian noise in the system and can be accounted for through the process noise covariance matrix \(Q\).

\section{Experimental results}
\label{experimentalresults}

 Two experiments which validate the proposed algorithms are presented. The game statistics of the experiments are tabulated in tables 1 and 2.
 
\begin{itemize}
\item \textit{Experiment 1}
\begin{table}[h]
\begin{tabular}
{|c|c|c|}
\hline
\((x_{p_0},y_{p_0}),V_p\) & (114.1,74.14), 10 \\
\hline
\((x_{e_0},y_{e_0}), V\) & (32.47,231.3), 8 \\
\hline
\((x_T,y_T),  \Delta T\) & (127.7,98.8), 0.8 \\
\hline
Diagonal elements of \(R\) & (64,64,1.5)\\
\hline
diagonal elements of \(Q\)& (10,10,0)\\
\hline
diagonal elements of \(P_0\)& (64,64,1.5)\\
\hline
\(Dist(T,I_0)\) & 83.34\\
\hline
\(Dist(T,I_f)\) (simulation) & 78.91\\
\hline
\(Dist(T,I_f)\) (experiment) & 71.47\\
\hline
\(P.I\) (Simulation)& 0.9468\\
\hline
\(P.I\) (Experiment)& 0.8569\\
\hline
\end{tabular}\label{experiment1}
\end{table}
  \item \textit{Experiment 2}
  \begin{table}[h]
\begin{tabular}
{|c|c|c|}
\hline
\((x_{p_0},y_{p_0}),V_p\) & (87.16,69.77), 10 \\
\hline
\((x_{e_0},y_{e_0}), V\) & (60.08,238.5887), 8 \\
\hline
\((x_T,y_T),  \Delta T\) & (119.9,132.5), 0.9 \\
\hline
Diagonal elements of \(R\)& (64,64,1)\\
\hline
Diagonal elements of \(Q\) & (10,10,0)\\
\hline
Diagonal elements of \(P_0\)& (64,64,1)\\
\hline
\(Dist(T,I_0)\) & 40.36\\
\hline
\(Dist(T,I_f)\) (simulation) & 40.05\\
\hline
\(Dist(T,I_f)\) (experiment) & 35.25\\
\hline
\(P.I \) (Simulation)& 0.9923\\
\hline
\(P.I \) (Experiment) & 0.8734\\
\hline
\end{tabular}\label{experiment2}
\end{table} 
 \end{itemize}
 Evader may lose an otherwise winning game even if pursuer is  playing sub-optimally because of practical limitations causing evader to take sub-optimal path. Same is the case with pursuer. Both the robots deviate from their respective simulation paths (refer figures \ref{KF1game1} and \ref{KF1game2}). If  limitations on evader's motion do not allow free maneuver of evader, pursuer intercepts evader at a point farther from the initial interception point (if pursuer has better maneuverability compared to that of evader). Same is the case with the evader. If pursuer is limited by maneuverability constraints, pursuer cannot pursue interception point corresponding to the estimates of Kalman filter at each instant. In that case, evader reaches a closer point to target than in simulation.
\begin{figure}[thpb]
   
\includegraphics[width=9cm]{Figures/gameexp.eps}
	\caption{Experimental versus simulation results. Black circles indicate approximate sizes of robots- Experiment 1}\label{KF1game1}
\end{figure}
\begin{figure}[thbp]
   \includegraphics[width=4.3cm]{Figures/speedexp.eps}
    \hfill
   \includegraphics[width=4.3cm]{Figures/varianceexp.eps}
 \caption{plots of (a) measured, estimated and true values of speed (b) auto-covariances of the states- Experiment 1}\label{kf1speed}
  \end{figure}
 
 \begin{figure}
\includegraphics[width=9cm]{Figures/gameexp2.eps}
\caption{Experimental versus simulation results. Black circles indicate approximate sizes of robots- Experiment 2}\label{KF1game2}
\end{figure}
 
 
 \begin{figure}[thbp]
   \includegraphics[width=4.3cm]{Figures/speedexp2.eps}
    \hfill
   \includegraphics[width=4.3cm]{Figures/varianceexp2.eps}
 \caption{plots of (a) measured, estimated and true values of speed (b) auto-covariances of the states- Experiment 2}\label{kf1speed2}
  \end{figure}

Figures \ref{kf1speed}, \ref{kf1speed2} validate the satisfactory operation of the Kalman filter designed to estimate evader's position and  speed. Like in simulations, Kalman filter was able to use the measurements of \(V\) to improve the estimates. In both the experiments, pursuer was able to intercept evader at a point close to initial interception point.  So, if the initial distance between target and pursuer is small and target is in pursuer's dominance region, pursuer can win the game by pursuing interception point corresponding to estimates of evader's position and speed.  

\section{Conclusion and future work}\label{conclusion}
In this work, Kalman filter to estimate evader's position and speed was designed. From simulations and experimental results, we argued that heading towards interception point corresponding to estimates of position and  speed of evader is a reliable strategy for the pursuer given pursuer is initially close to target. This simulation study will help put approximate  bounds on the distance of evader to the target at the beginning of the game for given positions of pursuer and target considering the sub-optimal play of pursuer. %No constraints on the evader's initial distance from the target in order for pursuer to win the game in-spite of his sub-optimal play have been established. Hence, 
The future work points to finding bounds on minimum initial distance between target and evader in order to guarantee success for pursuer when measurements are associated with noise.

\begin{thebibliography}{00}
\bibitem{b1} R. Isaacs, Differential Games: A Mathematical Theory
with Application to Warfare and Pursuit, Control and
Optimization. John Wiley and Sons, Inc. 1965.
\bibitem{b2}  Venkatesan, R. H., \& Sinha, N. K. (2014). The target guarding problem revisited: Some interesting revelations. In IFAC Proceedings Volumes (IFAC-PapersOnline) (Vol. 19, pp. 1556–1561). IFAC Secretariat. https://doi.org/10.3182/20140824-6-ZA-1003.02297
\bibitem{b3} R. Harini Venkatesan and N. K. Sinha, "A New Guidance Law for the Defense Missile of Nonmaneuverable Aircraft," in IEEE Transactions on Control Systems Technology, vol. 23, no. 6, pp. 2424-2431, Nov. 2015.
\bibitem{b4} D. Li and J. B. Cruz, "Defending an Asset: A Linear Quadratic Game Approach," in IEEE Transactions on Aerospace and Electronic Systems, vol. 47, no. 2, pp. 1026-1044, April 2011.
%\bibitem{b5} D. W. Oyler and A. R. Girard, "Dominance regions in the Homicidal Chauffeur Problem," 2016 American Control Conference (ACC), Boston, MA, 2016, pp. 2494-2499.
\bibitem{b5} J. Fan, J. Ruan, Y. Liang and L. Tang, "An iterative learning process based on Bayesian principle in pursuit-evasion games," Proceedings of the 29th Chinese Control Conference, Beijing, 2010, pp. 52-55.
\bibitem{b6} P. Zarchan and H. Musoff, Fundamentals of Kalman Filtering: A Practical Approach. American Institute of Aeronautics and Astronautics,
Virginia, 2000.
\bibitem{b7} H. Huang, J. Ding, W. Zhang, and C.J. Tomlin. A differential game approach
to planning in adversarial scenarios: a case study on capture-the-flag.
In Proceedings of the IEEE International Conference on Robotics
and Automation, Shanghai, China, 2011.
\bibitem{b8}Dongxu Li and J. B. Cruz, "A two-player stochastic pursuit-evasion differential game," 2007 46th IEEE Conference on Decision and Control, New Orleans, LA, 2007, pp. 4057-4062.
doi: 10.1109/CDC.2007.4434763
\bibitem{patcher2014} M. Pachter, E. Garcia and D. W. Casbeer, "Active target defense differential game," 2014 52nd Annual Allerton Conference on Communication, Control, and Computing (Allerton), Monticello, IL, 2014, pp. 46-53.
\bibitem{b9} Meir Pachter, Eloy Garcia, and David W. Casbeer.  "Differential Game of Guarding a Target", Journal of Guidance, Control, and Dynamics, Vol. 40, No. 11 (2017), pp. 2991-2998.
\bibitem{b10} D. Li and J. B. Cruz, "Defending an Asset: A Linear Quadratic Game Approach," in IEEE Transactions on Aerospace and Electronic Systems, vol. 47, no. 2, pp. 1026-1044, April 2011.
\bibitem{b11} J. Mohanan, S. R. Manikandasriram, R. Harini Venkatesan and B. Bhikkaji, "Toward Real-Time Autonomous Target Area Protection: Theory and Implementation," in IEEE Transactions on Control Systems Technology.
\bibitem{b12} R. Vidal, O. Shakernia, H. J. Kim, D. H. Shim and S. Sastry, "Probabilistic pursuit-evasion games: theory, implementation, and experimental evaluation," in IEEE Transactions on Robotics and Automation, vol. 18, no. 5, pp. 662-669, Oct 2002.
\bibitem{b13} J. P. Hespanha, M. Prandini and S. Sastry, "Probabilistic pursuit-evasion games: a one-step Nash approach," Proceedings of the 39th IEEE Conference on Decision and Control (Cat. No.00CH37187), Sydney, NSW, 2000, pp. 2272-2277 vol.3.
\bibitem{b14} Paul J. Nahin, The Mathematics of Pursuit and Evasion. Princeton University Press, 2007.
\bibitem{b15} Jean Walrand, Elijah Polak and Hoam Chung, "Harbor Attack: A Pursuit Evasion Game," Proceedings of the 49th Annual Allerton Conference on Communication, Control, and Computing (Allerton), 2011, pp. 1584-1591.
\bibitem{b16} Ahmad A. Al-Talabi, "Multi-player pursuit-evasion differential game with equal speed," 2017 International Automatic Control Conference (CACS), 2017, pp. 1-6.
\bibitem{b17} Wei Li, "A Dynamics Perspective of Pursuit-Evasion: Capturing and Escaping When the Pursuer Runs Faster Than the Agile Evader,"  IEEE Transactions on Automatic Control, Jan 2017, Vol 62, pp. 451-457.
\bibitem{b18} S.D. Bopardikar, F.Bullo, J.P. Hespanha, "On Discrete-time pursuit evasion games with sensing limitations,"  IEEE Transactions on Robotics, 2008, Vol 24, No.6, pp. 1429-1439.
\bibitem{b19} M. Foley and W. Schmitendorf, "A class of differential games with two pursuers versus one evader,"  IEEE Transactions on Automatic Control, 1974, Vol 19, No.3, pp. 239-243.
\bibitem{b20} Y. Ho, A. Bryson and S. Baron, "Differential games and Optimal pursuit evasion strategies,"  IEEE Transactions on Automatic Control, 1965, Vol 10, No.4, pp. 385-389.
\bibitem{b21} Shen Wang, Brian Mac Namee, "Evaluating citywide bus service reliability using noisy GPS data," 2017 International Smart Cities Conference (ISC2), 2017, pp. 1-6.
\bibitem{b22} Andrew W.R. Soundy, Bradley J. Panckhurst, Tim C.A. Molteno "Enhanced noise models for GPS positioning," 2015 6th International Conference on Automation, Robotics and Applications (ICARA), 2015 , pp. 28 - 33.
\end{thebibliography} 	 

\end{document}
