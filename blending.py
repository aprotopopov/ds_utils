import numpy as np
import pandas as pd
import datetime as dt

def get_clf_name(clf):
   return str(clf)[:str(clf).find('(')]    

def get_train_test(X_train, y_train, idx_fit, idx_eval):
    if type(X_train) == pd.core.frame.DataFrame:
        X_fit = X_train.iloc[idx_fit]
        X_eval = X_train.iloc[idx_eval]
    else:
        X_fit = X_train[idx_fit]
        X_eval = X_train[idx_eval]

    if type(y_train) == np.ndarray:
        y_fit = y_train[idx_fit]
        y_eval = y_train[idx_eval]
    else:
        y_fit = y_train.iloc[idx_fit]
        y_eval = y_train.iloc[idx_eval]

    return X_fit, X_eval, y_fit, y_eval


def blending(X_train, y_train, X_test, clfs, cv, verbose_xgb=False, scoring=None,
    stop_rounds=100, xgb_metric='auc'):
    if scoring is None:
        print('Enter scoring function')
        return

    train_preds = np.zeros(X_train.shape[0])
    scores = []

    dataset_blend_test_full = np.zeros((X_test.shape[0], len(clfs)))
    train_preds = np.zeros((X_train.shape[0], len(clfs)))
    print('{} folds with {} clfs, total {} fits'.format(cv.n_folds, len(clfs),
        (cv.n_folds) * len(clfs)))

    for j, clf in enumerate(clfs):
        dataset_blend_test = np.zeros((X_test.shape[0], cv.n_folds))
        clf_name = get_clf_name(clf)
        print("Fitting", clf_name)
        for i, (idx_fit, idx_eval) in enumerate(cv):
            print ("Fold", i)
            start_time = dt.datetime.now()
            X_fit, X_eval, y_fit, y_eval = get_train_test(X_train, y_train, 
                idx_fit, idx_eval)

            if clf_name.startswith("XGB"):
                clf.fit(X_fit, y_fit, early_stopping_rounds=stop_rounds, 
                    eval_metric=xgb_metric, verbose=verbose_xgb, 
                    eval_set=[(X_fit, y_fit), (X_eval, y_eval)])
                print('XGB best score {} with {} iterations'.format(
                    clf.best_score, clf.best_iteration))
            else:
                clf.fit(X_fit, y_fit)

            y_submission = clf.predict_proba(X_eval)[:, 1]
            score = scoring(y_eval, y_submission)
            scores.append(score)
            train_preds[idx_eval, j] = y_submission
            dataset_blend_test[:, i] = clf.predict_proba(X_test)[:, 1]
            print('iteration {} is finished, {} seconds, score {}'.format(i, 
                (dt.datetime.now() - start_time).total_seconds(), score))
        dataset_blend_test_full[:, j] = dataset_blend_test.mean(axis=1)

    print('mean: {}, std: {}'.format(np.mean(scores), np.std(scores)))
    print('full score: {}'.format(scoring(y_train, train_preds.mean(axis=1))))

    return train_preds, dataset_blend_test_full
